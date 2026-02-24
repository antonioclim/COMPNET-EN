from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def build(loss=20, delay=None):
    net = Mininet(controller=OVSController, link=TCLink, autoSetMacs=True)

    c0 = net.addController("c0")
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    s1 = net.addSwitch("s1")

    link_opts = {"loss": float(loss)}
    if delay:
        link_opts["delay"] = str(delay)

    net.addLink(h1, s1, **link_opts)
    net.addLink(s1, h2, **link_opts)

    net.start()
    return net

def main():
    setLogLevel("info")
    net = build(loss=20, delay=None)
    print("[topo] network started. Use CLI if needed.")
    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
