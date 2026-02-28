"""
Advanced Os-Ken policy controller (optional, extra)

This file is intentionally *extra* and does not replace the baseline controller:
  - S06_Part02C_Script_SDNOS_Ken_Controller.py

Pedagogical intent
------------------
The baseline controller in Part 2 introduces the absolute minimum logic needed
to install OpenFlow rules. This advanced controller adds three concepts that
often matter in real deployments:

1) **Policy as data**: an explicit allowlist / blocklist (host roles).
2) **Rule ageing**: idle/hard timeouts to prevent flow-table buildup.
3) **Fallback behaviour**: a small learning-switch path for unspecified traffic,
   so the network is not “dead by default”.

Topology assumption
-------------------
Matches S06_Part02B_Script_SDN_Topo_Switch.py:

    h1 ---- s1 ---- h2
             |
             +---- h3

- h1: 10.0.10.1/24
- h2: 10.0.10.2/24
- h3: 10.0.10.3/24

Default policy
--------------
- Allow all IPv4 traffic between h1 and h2.
- Block IPv4 traffic to/from h3.
- Optionally allow UDP to h3 (toggle via ALLOW_UDP_TO_H3 env var).

Run
---
In one terminal (controller):

  # Either of the following commands may work depending on your installation.
  osken-manager S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py
  ryu-manager   S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py

In another terminal (topology):

  sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py

Optional environment toggles
----------------------------
- ALLOW_UDP_TO_H3=1         (default: 0)
- FLOW_IDLE_TIMEOUT=60      (default: 60)
- FLOW_HARD_TIMEOUT=300     (default: 300)

Note
----
This is a teaching controller, not a production firewall.
"""

from __future__ import annotations

import os
from typing import Dict

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import MAIN_DISPATCHER, set_ev_cls
from os_ken.lib.packet import packet
from os_ken.lib.packet import ethernet, arp, ipv4
from os_ken.lib.packet import ether_types
from os_ken.ofproto import ofproto_v1_3


H1_IP = "10.0.10.1"
H2_IP = "10.0.10.2"
H3_IP = "10.0.10.3"

PERMITTED_HOSTS = {H1_IP, H2_IP}
PROTECTED_HOST = H3_IP

ALLOW_UDP_TO_H3 = os.getenv("ALLOW_UDP_TO_H3", "0").strip().lower() in {"1", "true", "yes"}
FLOW_IDLE_TIMEOUT = int(os.getenv("FLOW_IDLE_TIMEOUT", "60"))
FLOW_HARD_TIMEOUT = int(os.getenv("FLOW_HARD_TIMEOUT", "300"))

# Priorities: bigger number = stronger policy.
PRIORITY_DROP = 200
PRIORITY_PERMIT = 100
PRIORITY_L2_LEARNING = 10


class AdvancedPolicyController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mac_to_port: Dict[str, int] = {}

    def add_flow(self, datapath, priority, match, actions, idle_timeout=0, hard_timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout,
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, MAIN_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        self.logger.info("Switch connected (datapath id=%s)", datapath.id)

        # Table-miss: send unknown packets to controller.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # ------------------------------------------------------------------
        # Policy rules (IPv4)
        # ------------------------------------------------------------------

        # Permit IPv4 between h1 and h2 (bidirectional).
        for src, dst in [(H1_IP, H2_IP), (H2_IP, H1_IP)]:
            match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src, ipv4_dst=dst)
            # Use the topology port layout:
            #   s1-eth1 <-> h1
            #   s1-eth2 <-> h2
            out_port = 2 if dst == H2_IP else 1
            actions = [parser.OFPActionOutput(out_port)]
            self.add_flow(
                datapath,
                PRIORITY_PERMIT,
                match,
                actions,
                idle_timeout=FLOW_IDLE_TIMEOUT,
                hard_timeout=FLOW_HARD_TIMEOUT,
            )
            self.logger.info("Permit rule installed: %s -> %s (out_port=%s)", src, dst, out_port)

        # Default: block IPv4 to/from h3.
        for src, dst in [
            (H1_IP, H3_IP),
            (H2_IP, H3_IP),
            (H3_IP, H1_IP),
            (H3_IP, H2_IP),
        ]:
            match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src, ipv4_dst=dst)
            self.add_flow(datapath, PRIORITY_DROP, match, actions=[])
            self.logger.info("Drop rule installed: %s -> %s", src, dst)

        # Optional: allow UDP to/from h3 (only if explicitly enabled).
        if ALLOW_UDP_TO_H3:
            ip_proto_udp = 17
            for src, dst, out_port in [
                (H1_IP, H3_IP, 3),
                (H2_IP, H3_IP, 3),
                (H3_IP, H1_IP, 1),
                (H3_IP, H2_IP, 2),
            ]:
                match = parser.OFPMatch(
                    eth_type=0x0800,
                    ipv4_src=src,
                    ipv4_dst=dst,
                    ip_proto=ip_proto_udp,
                )
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(
                    datapath,
                    PRIORITY_PERMIT + 10,  # stronger than generic permit
                    match,
                    actions,
                    idle_timeout=FLOW_IDLE_TIMEOUT,
                    hard_timeout=FLOW_HARD_TIMEOUT,
                )
                self.logger.info("UDP exception installed: %s -> %s (out_port=%s)", src, dst, out_port)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
        Fallback learning-switch logic for traffic not explicitly covered by the policy.

        Crucial detail: policy flows have higher priority, therefore:
        - permitted h1<->h2 flows match before this handler does anything
        - blocked h? <-> h3 flows are dropped before reaching here
        """
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        # Drop LLDP and other control frames.
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        src = eth.src
        dst = eth.dst
        in_port = msg.match["in_port"]

        # Learn source MAC.
        self.mac_to_port[dpid][src] = in_port

        # ARP handling: flood and learn (standard learning switch behaviour).
        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            out_port = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(out_port)]
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data,
            )
            datapath.send_msg(out)
            return

        # IPv4: apply a light L2 learning behaviour.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install a short-lived L2 rule to reduce controller load.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(
                datapath,
                PRIORITY_L2_LEARNING,
                match,
                actions,
                idle_timeout=30,
                hard_timeout=0,
            )

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=None if msg.buffer_id != ofproto.OFP_NO_BUFFER else msg.data,
        )
        datapath.send_msg(out)
