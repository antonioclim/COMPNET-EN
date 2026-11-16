"""Regression checks for the VM setup fixes, without privileged networking.

The controller is executed against a small in-memory OpenFlow message recorder.
These checks exercise policy precedence, persistence and event registration;
they do not emulate a switch or establish native OS-Ken/Mininet acceptance.
OVS verification tests use a fake ovs-vsctl executable and never reset OVS.
Run: python3 -m unittest discover -s 00_TOOLS/qa -p test_mininet_setup_contracts.py -v
"""

from __future__ import annotations

import importlib.util
import logging
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
CONTROLLER = ROOT / "04_SEMINARS/S06/2_sdn/S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py"


def load_controller(allow_udp: bool):
    names = [
        "os_ken", "os_ken.base", "os_ken.base.app_manager", "os_ken.controller",
        "os_ken.controller.ofp_event", "os_ken.controller.handler", "os_ken.lib",
        "os_ken.lib.packet", "os_ken.lib.packet.packet", "os_ken.lib.packet.ethernet",
        "os_ken.lib.packet.arp", "os_ken.lib.packet.ipv4", "os_ken.lib.packet.ether_types",
        "os_ken.ofproto", "os_ken.ofproto.ofproto_v1_3",
    ]
    modules = {name: types.ModuleType(name) for name in names}
    for name, module in modules.items():
        if "." in name:
            parent, leaf = name.rsplit(".", 1)
            setattr(modules[parent], leaf, module)

    class OSKenApp:
        def __init__(self, *args, **kwargs):
            self.logger = logging.getLogger("controller-test")

    def register(event, dispatcher):
        def decorate(function):
            function.observed_event = event
            function.observed_dispatcher = dispatcher
            return function
        return decorate

    modules["os_ken.base.app_manager"].OSKenApp = OSKenApp
    handler = modules["os_ken.controller.handler"]
    handler.CONFIG_DISPATCHER = "config"
    handler.MAIN_DISPATCHER = "main"
    handler.set_ev_cls = register
    events = modules["os_ken.controller.ofp_event"]
    events.EventOFPSwitchFeatures = type("EventOFPSwitchFeatures", (), {})
    events.EventOFPPacketIn = type("EventOFPPacketIn", (), {})
    modules["os_ken.ofproto.ofproto_v1_3"].OFP_VERSION = 4
    spec = importlib.util.spec_from_file_location("tested_sdn_controller", CONTROLLER)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules), patch.dict(os.environ, {"ALLOW_UDP_TO_H3": str(int(allow_udp)), "FLOW_IDLE_TIMEOUT": "60", "FLOW_HARD_TIMEOUT": "300"}):
        spec.loader.exec_module(module)
    return module


class Parser:
    @staticmethod
    def OFPMatch(**fields):
        return fields

    @staticmethod
    def OFPActionOutput(port, max_len=None):
        return types.SimpleNamespace(port=port, max_len=max_len)

    @staticmethod
    def OFPInstructionActions(kind, actions):
        return types.SimpleNamespace(kind=kind, actions=actions)

    @staticmethod
    def OFPFlowMod(**fields):
        return types.SimpleNamespace(**fields)


def initial_rules(allow_udp: bool):
    module = load_controller(allow_udp)
    messages = []
    datapath = types.SimpleNamespace(
        id=1, ofproto_parser=Parser,
        ofproto=types.SimpleNamespace(OFPP_CONTROLLER=0xFFFFFFFD, OFPCML_NO_BUFFER=0xFFFF, OFPIT_APPLY_ACTIONS=4),
        send_msg=messages.append,
    )
    app = module.AdvancedPolicyController()
    app.switch_features_handler(types.SimpleNamespace(msg=types.SimpleNamespace(datapath=datapath)))
    return module, messages


def selected_ports(rules, src, dst, protocol, elapsed=0):
    packet = dict(eth_type=0x0800, ipv4_src=src, ipv4_dst=dst, ip_proto=protocol)
    candidates = [
        rule for rule in rules
        if all(packet.get(key) == value for key, value in rule.match.items())
        and (rule.hard_timeout == 0 or elapsed < rule.hard_timeout)
        and (rule.idle_timeout == 0 or elapsed < rule.idle_timeout)
    ]
    rule = max(candidates, key=lambda entry: entry.priority)
    return [action.port for instruction in rule.instructions for action in instruction.actions]


class ControllerPolicyTests(unittest.TestCase):
    def test_features_are_observed_during_configuration(self):
        module = load_controller(False)
        self.assertEqual(module.AdvancedPolicyController.switch_features_handler.observed_dispatcher, "config")
        self.assertEqual(module.AdvancedPolicyController.OFP_VERSIONS, [4])

    def test_default_h1_h2_bidirectional_traffic_is_permitted(self):
        module, rules = initial_rules(False)
        for protocol in (1, 6, 17):
            self.assertEqual(selected_ports(rules, module.H1_IP, module.H2_IP, protocol), [2])
            self.assertEqual(selected_ports(rules, module.H2_IP, module.H1_IP, protocol), [1])

    def test_protected_host_is_blocked_without_exception(self):
        module, rules = initial_rules(False)
        for peer in (module.H1_IP, module.H2_IP):
            for protocol in (1, 6, 17):
                self.assertEqual(selected_ports(rules, peer, module.H3_IP, protocol), [])
                self.assertEqual(selected_ports(rules, module.H3_IP, peer, protocol), [])

    def test_udp_exception_wins_in_both_directions(self):
        module, rules = initial_rules(True)
        for peer, peer_port in ((module.H1_IP, 1), (module.H2_IP, 2)):
            self.assertEqual(selected_ports(rules, peer, module.H3_IP, 17), [3])
            self.assertEqual(selected_ports(rules, module.H3_IP, peer, 17), [peer_port])
            for protocol in (1, 6):
                self.assertEqual(selected_ports(rules, peer, module.H3_IP, protocol), [])
                self.assertEqual(selected_ports(rules, module.H3_IP, peer, protocol), [])

    def test_udp_policy_does_not_expire_into_permanent_drop(self):
        module, rules = initial_rules(True)
        for elapsed in (61, 301, 3600):
            self.assertEqual(selected_ports(rules, module.H1_IP, module.H3_IP, 17, elapsed), [3])
            self.assertEqual(selected_ports(rules, module.H3_IP, module.H1_IP, 17, elapsed), [1])


class OVSVerificationTests(unittest.TestCase):
    def run_verifier(self, stdout, exit_code):
        with tempfile.TemporaryDirectory() as directory:
            command = Path(directory) / "ovs-vsctl"
            command.write_text("#!/bin/sh\nprintf '%s' \"$FAKE_OVS_OUTPUT\"\nexit \"$FAKE_OVS_STATUS\"\n")
            command.chmod(0o755)
            environment = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], FAKE_OVS_OUTPUT=stdout, FAKE_OVS_STATUS=str(exit_code))
            return subprocess.run(
                ["bash", str(ROOT / "00_TOOLS/mininet/ovs_reset.sh"), "--verify", "--quiet"],
                env=environment, text=True, capture_output=True, timeout=5,
            )

    def test_database_failure_is_not_clean_state(self):
        result = self.run_verifier("", 1)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot read OVSDB", result.stderr)

    def test_successful_empty_database_is_clean(self):
        self.assertEqual(self.run_verifier("", 0).returncode, 0)

    def test_remaining_bridge_is_not_clean(self):
        self.assertNotEqual(self.run_verifier("s1\n", 0).returncode, 0)


if __name__ == "__main__":
    unittest.main()
