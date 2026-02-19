"""
Mininet topology: Triangle of 3 routers + 2 hosts
h1 connected to r1, h3 connected to r3, and three links r1–r2, r2–r3, r1–r3.

The router is a Mininet Node with IP forwarding enabled.
The student will configure static routes manually.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel


class LinuxRouter(Node):
    """A Mininet node with IP forwarding enabled (behaves as a real Linux router)."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable IPv4 forwarding
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        super(LinuxRouter, self).terminate()


class TriangleRoutingTopo(Topo):
    """Triangle topology r1–r2–r3, plus hosts h1 and h3."""
    def build(self):

        # Create the routers
        r1 = self.addNode('r1', cls=LinuxRouter)
        r2 = self.addNode('r2', cls=LinuxRouter)
        r3 = self.addNode('r3', cls=LinuxRouter)

        # Hosts
        h1 = self.addHost('h1')
        h3 = self.addHost('h3')

        # Host-router links
        self.addLink(h1, r1)
        self.addLink(h3, r3)

        # Triangle links
        self.addLink(r1, r2)
        self.addLink(r2, r3)
        self.addLink(r1, r3)


def run():
    """
    Create the network, assign IP addresses and launch the CLI for configuration.
    Basic routes are added automatically so that h1 and h3 can ping each other.
    The student will modify / extend the routing later.
    """
    topo = TriangleRoutingTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    # Node references
    r1, r2, r3 = net.get('r1'), net.get('r2'), net.get('r3')
    h1, h3 = net.get('h1'), net.get('h3')

    # ------------------------------
    # IPv4 interface configuration
    # ------------------------------

    # h1 <-> r1
    h1.setIP("10.0.1.2/30", intf="h1-eth0")
    r1.setIP("10.0.1.1/30", intf="r1-eth0")

    # r1 <-> r2
    r1.setIP("10.0.12.1/30", intf="r1-eth1")
    r2.setIP("10.0.12.2/30", intf="r2-eth0")

    # r2 <-> r3
    r2.setIP("10.0.23.1/30", intf="r2-eth1")
    r3.setIP("10.0.23.2/30", intf="r3-eth1")   # FIX: r3-eth1, not r3-eth0

    # r1 <-> r3
    r1.setIP("10.0.13.1/30", intf="r1-eth2")
    r3.setIP("10.0.13.2/30", intf="r3-eth2")   # FIX: r3-eth2, not r3-eth1

    # r3 <-> h3
    r3.setIP("10.0.3.1/30", intf="r3-eth0")    # FIX: r3-eth0, not r3-eth2
    h3.setIP("10.0.3.2/30", intf="h3-eth0")

    # ------------------------------
    # Basic routes for h1 <-> h3 connectivity
    # ------------------------------

    # Default gateways for hosts
    h1.cmd("ip route add default via 10.0.1.1")
    h3.cmd("ip route add default via 10.0.3.1")

    # Static routes on routers, using the direct r1 <-> r3 link
    r1.cmd("ip route add 10.0.3.0/30 via 10.0.13.2")
    r3.cmd("ip route add 10.0.1.0/30 via 10.0.13.1")

    print("\n=== Topology has been started ===")
    print("IP configuration and basic routes are set.")
    print("You can now test directly: h1 ping 10.0.3.2")

    CLI(net)
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    run()
