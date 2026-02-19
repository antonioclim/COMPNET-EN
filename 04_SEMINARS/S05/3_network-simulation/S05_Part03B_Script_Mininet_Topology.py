"""
Mininet topology for the Computer Networks course
h1 ---- r1 ---- h2

This file defines a simple topology with two hosts and an
intermediary node used as a router. Students will configure
IP addresses, routes and test connectivity.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class LinuxRouter(Node):
    """
    A Mininet node that behaves as a real Linux router.
    IP forwarding is enabled at start-up.
    """
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # enable IPv4 forwarding
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        # optional: enable IPv6 forwarding
        self.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')

    def terminate(self):
        super(LinuxRouter, self).terminate()

class SimpleTopo(Topo):
    """
    Topology:
        h1 ----- r1 ----- h2
    """
    def build(self):

        # Create the router (a host with forwarding enabled)
        r1 = self.addNode('r1', cls=LinuxRouter)

        # Create the two hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Create the links
        self.addLink(h1, r1, intfName2='r1-eth0')
        self.addLink(h2, r1, intfName2='r1-eth1')

def run():
    """
    Start the network, assign IP addresses and launch the Mininet CLI.
    Students will continue the configuration from there.
    """
    topo = SimpleTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    # Host references
    h1 = net.get('h1')
    h2 = net.get('h2')
    r1 = net.get('r1')

    # ---------------- IPv4 ----------------
    # Assign addresses to interfaces
    h1.setIP('10.0.1.10/24', intf='h1-eth0')
    r1.setIP('10.0.1.1/24', intf='r1-eth0')

    h2.setIP('10.0.2.10/24', intf='h2-eth0')
    r1.setIP('10.0.2.1/24', intf='r1-eth1')

    # Optional IPv6
    # h1.setIP('2001:db8:10:1::10/64', intf='h1-eth0')
    # h2.setIP('2001:db8:10:2::10/64', intf='h2-eth0')
    # r1.setIP('2001:db8:10:1::1/64', intf='r1-eth0')
    # r1.setIP('2001:db8:10:2::1/64', intf='r1-eth1')

    # Configure default routes on hosts
    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.2.1')

    print("The network has been started. Use the CLI for additional configuration.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
