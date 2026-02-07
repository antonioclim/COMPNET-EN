"""
Controller OS-Ken simplu pentru topologia:
    h1 ---- s1 ---- h2
             |
             +---- h3

Comportament:
 - Traficul intre h1 (10.0.10.1) si h2 (10.0.10.2) este permis (flow-uri instalate).
 - Traficul catre h3 (10.0.10.3) este blocat (flow de tip drop).
"""

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ipv4, arp


class SimpleSwitch13(app_manager.OSKenApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # MAC-uri implicite Mininet (autoSetMacs=True):
    H1_MAC = "00:00:00:00:00:01"
    H2_MAC = "00:00:00:00:00:02"
    H3_MAC = "00:00:00:00:00:03"

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # dpid -> {mac -> port}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Apelat cand switch-ul se conecteaza la controller.
        Instalam o regula table-miss: orice pachet necunoscut este trimis la controller.
        """
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]
        self.add_flow(datapath, priority=0, match=match, actions=actions)
        self.logger.info("Table-miss flow instalat pe switch %s", datapath.id)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """Helper pentru a instala un flow in switch."""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS,
            actions
        )]

        if buffer_id is not None and buffer_id != ofproto.OFP_NO_BUFFER:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=inst
            )
        else:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=priority,
                match=match,
                instructions=inst
            )

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
        Apelat cand switch-ul trimite un pachet necunoscut la controller.
        - ARP: facem L2 simplu (learn + flood/forward).
        - IPv4: aplicam politica (permit h1<->h2, drop catre h3).
        """
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        in_port = msg.match['in_port']

        pkt = packet.Packet(data=msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        arp_pkt = pkt.get_protocol(arp.arp)

        src_mac = eth.src
        dst_mac = eth.dst

        # Inregistram portul pe care am vazut sursa
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src_mac] = in_port

        self.logger.info("PacketIn: dpid=%s eth_src=%s eth_dst=%s in_port=%s",
                         dpid, src_mac, dst_mac, in_port)

        # 1) Tratare ARP: fara politica speciala, doar L2 learning switch
        if arp_pkt:
            self.logger.info("ARP: %s -> %s (op=%s)",
                             arp_pkt.src_ip, arp_pkt.dst_ip, arp_pkt.opcode)

            # Daca stim portul pentru destinatar, trimitem direct
            if dst_mac in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst_mac]
            else:
                out_port = ofproto.OFPP_FLOOD

            actions = [parser.OFPActionOutput(out_port)]

            # Optional: putem instala si un flow low-priority pentru ARP,
            # dar pentru simplitate doar trimitem pachetul actual.
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)
            return

        # 2) Daca nu e IPv4, nu facem nimic special
        if not ipv4_pkt:
            return

        src_ip = ipv4_pkt.src
        dst_ip = ipv4_pkt.dst

        self.logger.info("IPv4: %s -> %s", src_ip, dst_ip)

        # Caz 1: trafic intre h1 (10.0.10.1) si h2 (10.0.10.2)
        if ((src_ip == "10.0.10.1" and dst_ip == "10.0.10.2") or
                (src_ip == "10.0.10.2" and dst_ip == "10.0.10.1")):

            # Porturi fizice presupuse:
            #   h1 -> port 1, h2 -> port 2, h3 -> port 3
            out_port = None
            if src_mac == self.H1_MAC and dst_mac == self.H2_MAC:
                out_port = 2
            elif src_mac == self.H2_MAC and dst_mac == self.H1_MAC:
                out_port = 1

            if out_port is None:
                # fallback: daca nu stim, incercam tabelul mac_to_port
                out_port = self.mac_to_port[dpid].get(
                    dst_mac,
                    ofproto.OFPP_FLOOD
                )

            actions = [parser.OFPActionOutput(out_port)]

            # Instalare flow pentru trafic specific (match pe IP src/dst)
            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_src=src_ip,
                ipv4_dst=dst_ip
            )

            self.add_flow(
                datapath,
                priority=10,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id
                if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )

            # Trimitem si pachetul actual daca nu e in buffer
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                out = parser.OFPPacketOut(
                    datapath=datapath,
                    buffer_id=ofproto.OFP_NO_BUFFER,
                    in_port=in_port,
                    actions=actions,
                    data=msg.data
                )
                datapath.send_msg(out)

            self.logger.info("Permis: %s -> %s prin portul %s",
                             src_ip, dst_ip, out_port)
            return

        # Caz 2: destinatia este h3 (10.0.10.3) -> blocam (drop)
        if dst_ip == "10.0.10.3":
            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_dst=dst_ip
            )
            actions = []  # lista goala => drop

            self.add_flow(
                datapath,
                priority=20,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id
                if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )

            self.logger.info("Blocare trafic catre %s (flow drop instalat)",
                             dst_ip)
            # Nu trimitem nici un packet-out: pachetul curent e dropp-uit.
            return

        # Caz implicit: nu facem nimic (sau doar log)
        self.logger.info("Trafic neacoperit explicit: %s -> %s (ignorat)",
                         src_ip, dst_ip)
