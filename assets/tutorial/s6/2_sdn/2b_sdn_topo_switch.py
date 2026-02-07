"""
Topologie Mininet pentru SDN:
    h1 ---- s1 ---- h2
             |
             +---- h3

s1 este un Open vSwitch controlat de un controller os-ken extern.
Hosturile au adrese in acelasi subnet 10.0.10.0/24.

Studentul va porni separat controllerul os-ken si va testa ping-ul intre hosturi.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


class SDNSimpleTopo(Topo):
    """Topologie simpla cu un singur switch si trei hosturi."""
    def build(self):
        # Cream un singur switch Open vSwitch
        s1 = self.addSwitch('s1')

        # Cream hosturile
        h1 = self.addHost('h1', ip='10.0.10.1/24')
        h2 = self.addHost('h2', ip='10.0.10.2/24')
        h3 = self.addHost('h3', ip='10.0.10.3/24')

        # Conectam hosturile la switch
        # Ordinea porturilor va fi:
        #   s1-eth1 <-> h1
        #   s1-eth2 <-> h2
        #   s1-eth3 <-> h3
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


def run():
    """
    Creeaza reteaua, seteaza controllerul ca RemoteController (os-ken)
    si lanseaza CLI-ul Mininet.

    Controllerul trebuie pornit separat, inainte sau dupa pornirea retelei,
    pe 127.0.0.1:6633.
    """
    topo = SDNSimpleTopo()

    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True  # MAC-urile vor fi 00:00:00:00:00:01 etc.
    )

    # Adaugam un controller extern (Os-Ken) pe 127.0.0.1:6633
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    net.start()
    info("\n=== Retea SDN pornita (h1, h2, h3, s1) ===\n")
    info("Controllerul trebuie sa ruleze pe 127.0.0.1:6633 (os-ken).\n")
    info("Incercati: h1 ping -c 3 10.0.10.2 si h1 ping -c 3 10.0.10.3\n\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
