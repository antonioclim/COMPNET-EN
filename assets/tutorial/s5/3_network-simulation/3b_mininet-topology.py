"""
Topologie Mininet pentru disciplina Retele de Calculatoare
h1 ---- r1 ---- h2

Acest fisier defineste o topologie simpla cu doua hosturi si un nod
intermediar folosit drept router. Studentii vor configura adrese IP,
rute si vor testa conectivitatea.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class LinuxRouter(Node):
    """
    Un nod Mininet care se comporta ca un router Linux real.
    Pentru asta activam IP forwarding in momentul initierii.
    """
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # activam forwardarea IPv4
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        # optional, pentru IPv6
        self.cmd('sysctl -w net.ipv6.conf.all.forwarding=1')

    def terminate(self):
        super(LinuxRouter, self).terminate()

class SimpleTopo(Topo):
    """
    Topologie:
        h1 ----- r1 ----- h2
    """
    def build(self):

        # Cream routerul (un host cu forwarding activat)
        r1 = self.addNode('r1', cls=LinuxRouter)

        # Cream cele doua hosturi
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Cream legaturile
        self.addLink(h1, r1, intfName2='r1-eth0')
        self.addLink(h2, r1, intfName2='r1-eth1')

def run():
    """
    Pornim reteaua, asignam adresele IP si lansam CLI-ul Mininet.
    Studentii vor continua configurarea.
    """
    topo = SimpleTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    # Referinte pentru hosturi
    h1 = net.get('h1')
    h2 = net.get('h2')
    r1 = net.get('r1')

    # ---------------- IPv4 ----------------
    # Asignam adrese pe interfete
    h1.setIP('10.0.1.10/24', intf='h1-eth0')
    r1.setIP('10.0.1.1/24', intf='r1-eth0')

    h2.setIP('10.0.2.10/24', intf='h2-eth0')
    r1.setIP('10.0.2.1/24', intf='r1-eth1')

    # Optional IPv6
    # h1.setIP('2001:db8:10:1::10/64', intf='h1-eth0')
    # h2.setIP('2001:db8:10:2::10/64', intf='h2-eth0')
    # r1.setIP('2001:db8:10:1::1/64', intf='r1-eth0')
    # r1.setIP('2001:db8:10:2::1/64', intf='r1-eth1')

    # Configuram rutele implicite pe hosturi
    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.2.1')

    print("Reteaua a fost pornita. Folositi CLI pentru configurari suplimentare.")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
