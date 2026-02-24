"""
Mininet topology for SDN:
    h1 ---- s1 ---- h2
             |
             +---- h3

s1 is an Open vSwitch controlled by an external Os-Ken controller.
Hosts share the same 10.0.10.0/24 subnet.

The student will start the Os-Ken controller separately and test ping between hosts.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


class SDNSimpleTopo(Topo):
    """Simple topology with a single switch and three hosts."""
    def build(self):
        # Create a single Open vSwitch
        s1 = self.addSwitch('s1')

        # Create the hosts
        h1 = self.addHost('h1', ip='10.0.10.1/24')
        h2 = self.addHost('h2', ip='10.0.10.2/24')
        h3 = self.addHost('h3', ip='10.0.10.3/24')

        # Connect hosts to the switch
        # Port order will be:
        #   s1-eth1 <-> h1
        #   s1-eth2 <-> h2
        #   s1-eth3 <-> h3
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


def run():
    """
    Create the network, set the controller as RemoteController (Os-Ken)
    and launch the Mininet CLI.

    The controller must be started separately, before or after the network,
    on 127.0.0.1:6633.
    """
    topo = SDNSimpleTopo()

    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True  # MACs will be 00:00:00:00:00:01 etc.
    )

    # Add an external controller (Os-Ken) on 127.0.0.1:6633
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    net.start()
    info("\n=== SDN network started (h1, h2, h3, s1) ===\n")
    info("The controller must be running on 127.0.0.1:6633 (Os-Ken).\n")
    info("Try: h1 ping -c 3 10.0.10.2 and h1 ping -c 3 10.0.10.3\n\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
