#!/usr/bin/env python3
import sys
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1 >/dev/null")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0 >/dev/null")
        super().terminate()


def add_ip(node, intf, cidr):
    node.cmd(f"ip addr add {cidr} dev {intf}")


def set_default_route(host, via):
    host.cmd(f"ip route add default via {via}")


def build_net():
    net = Mininet(link=TCLink, controller=None, waitConnected=True)

    info("*** Nodes\n")
    r1 = net.addHost("r1", cls=LinuxRouter)
    r2 = net.addHost("r2", cls=LinuxRouter)
    r3 = net.addHost("r3", cls=LinuxRouter)

    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    h3 = net.addHost("h3")

    info("*** Links (triangle + LANs)\n")
    net.addLink(r1, r2, intfName1="r1-eth1", intfName2="r2-eth1")
    net.addLink(r1, r3, intfName1="r1-eth2", intfName2="r3-eth1")
    net.addLink(r2, r3, intfName1="r2-eth2", intfName2="r3-eth2")

    net.addLink(h1, r1, intfName2="r1-eth0")
    net.addLink(h2, r2, intfName2="r2-eth0")
    net.addLink(h3, r3, intfName2="r3-eth0")

    net.start()

    info("*** IP addressing (LANs)\n")
    add_ip(r1, "r1-eth0", "10.1.0.1/24")
    add_ip(h1, "h1-eth0", "10.1.0.2/24")
    set_default_route(h1, "10.1.0.1")

    add_ip(r2, "r2-eth0", "10.2.0.1/24")
    add_ip(h2, "h2-eth0", "10.2.0.2/24")
    set_default_route(h2, "10.2.0.1")

    add_ip(r3, "r3-eth0", "10.3.0.1/24")
    add_ip(h3, "h3-eth0", "10.3.0.2/24")
    set_default_route(h3, "10.3.0.1")

    info("*** IP addressing (inter-router links)\n")
    add_ip(r1, "r1-eth1", "10.12.0.1/24")
    add_ip(r2, "r2-eth1", "10.12.0.2/24")

    add_ip(r1, "r1-eth2", "10.13.0.1/24")
    add_ip(r3, "r3-eth1", "10.13.0.3/24")

    add_ip(r2, "r2-eth2", "10.23.0.2/24")
    add_ip(r3, "r3-eth2", "10.23.0.3/24")

    return net, r1, r2, r3, h1, h2, h3


def scenario_link_down(net, r1, r2, r3):
    info("*** Scenario: link-down (r1-r2 fails, traffic routes via r3)\n")

    # r1 <-> r2 via r3 (bypass)
    r1.cmd("ip route add 10.2.0.0/24 via 10.13.0.3 dev r1-eth2")
    r2.cmd("ip route add 10.1.0.0/24 via 10.23.0.3 dev r2-eth2")

    # optional: full connectivity between all LANs
    r1.cmd("ip route add 10.3.0.0/24 via 10.13.0.3 dev r1-eth2")
    r2.cmd("ip route add 10.3.0.0/24 via 10.23.0.3 dev r2-eth2")
    r3.cmd("ip route add 10.1.0.0/24 via 10.13.0.1 dev r3-eth1")
    r3.cmd("ip route add 10.2.0.0/24 via 10.23.0.2 dev r3-eth2")

    info("*** Bringing down link r1-r2 (both ends)\n")
    r1.cmd("ip link set r1-eth1 down")
    r2.cmd("ip link set r2-eth1 down")

    info("*** Link r1-r2 is DOWN. Traffic must bypass via r3.\n")


def scenario_asymmetric(net, r1, r2, r3):
    info("*** Scenario: asymmetric routing (only r1 has a route to r2)\n")

    # r1 knows how to reach r2's LAN via r2 (directly)
    r1.cmd("ip route add 10.2.0.0/24 via 10.12.0.2 dev r1-eth1")

    # r2 does NOT receive a return route towards 10.1.0.0/24
    # (no default route on r2 either, to make the "no return" case clear)

    # optional: do not set alternative routes via r3 so as to avoid interference
    info("*** r1 -> 10.2.0.0/24 is configured, but r2 has no route -> 10.1.0.0/24.\n")
    info("*** Ping h1->h2 will fail (the reply has no return route).\n")


def main():
    setLogLevel("info")
    if len(sys.argv) < 2:
        print("Usage: sudo python3 tringle-net.py <link-down|asymmetric>")
        sys.exit(1)

    mode = sys.argv[1].strip().lower()
    if mode not in {"link-down", "asymmetric"}:
        print("Mode must be one of: link-down, asymmetric")
        sys.exit(1)

    net, r1, r2, r3, h1, h2, h3 = build_net()

    try:
        if mode == "link-down":
            scenario_link_down(net, r1, r2, r3)
        else:
            scenario_asymmetric(net, r1, r2, r3)

        info("*** Entering Mininet CLI. Suggestions:\n")
        info("  h1 ping -c 2 10.2.0.2\n")
        info("  r1 ip route\n  r2 ip route\n  r3 ip route\n")
        CLI(net)
    finally:
        net.stop()


if __name__ == "__main__":
    main()
