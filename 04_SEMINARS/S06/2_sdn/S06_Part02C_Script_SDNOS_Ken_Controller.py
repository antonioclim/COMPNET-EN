"""
Simple Os-Ken controller for the topology:
    h1 ---- s1 ---- h2
             |
             +---- h3

Behaviour:
 - Traffic between h1 (10.0.10.1) and h2 (10.0.10.2) is permitted (flows installed).
 - Traffic towards h3 (10.0.10.3) is blocked (drop flow).
"""

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ipv4, arp


class SimpleSwitch13(app_manager.OSKenApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Default Mininet MACs (autoSetMacs=True):
    H1_MAC = "00:00:00:00:00:01"
    H2_MAC = "00:00:00:00:00:02"
    H3_MAC = "00:00:00:00:00:03"

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # dpid -> {mac -> port}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Called when the switch connects to the controller.
        Install a table-miss rule: any unknown packet is sent to the controller.
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
        self.logger.info("Table-miss flow installed on switch %s", datapath.id)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """Helper to install a flow in the switch."""
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
        Called when the switch sends an unknown packet to the controller.
        - ARP: simple L2 handling (learn + flood/forward).
        - IPv4: apply the policy (permit h1<->h2, drop towards h3).
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

        # Record the port on which the source was seen
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src_mac] = in_port

        self.logger.info("PacketIn: dpid=%s eth_src=%s eth_dst=%s in_port=%s",
                         dpid, src_mac, dst_mac, in_port)

        # 1) ARP handling: no special policy, just L2 learning switch
        if arp_pkt:
            self.logger.info("ARP: %s -> %s (op=%s)",
                             arp_pkt.src_ip, arp_pkt.dst_ip, arp_pkt.opcode)

            # If we know the port for the destination, send directly
            if dst_mac in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst_mac]
            else:
                out_port = ofproto.OFPP_FLOOD

            actions = [parser.OFPActionOutput(out_port)]

            # Optionally a low-priority ARP flow could be installed,
            # but for simplicity only the current packet is forwarded.
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)
            return

        # 2) If not IPv4, no special handling
        if not ipv4_pkt:
            return

        src_ip = ipv4_pkt.src
        dst_ip = ipv4_pkt.dst

        self.logger.info("IPv4: %s -> %s", src_ip, dst_ip)

        # Case 1: traffic between h1 (10.0.10.1) and h2 (10.0.10.2)
        if ((src_ip == "10.0.10.1" and dst_ip == "10.0.10.2") or
                (src_ip == "10.0.10.2" and dst_ip == "10.0.10.1")):

            # Assumed physical ports:
            #   h1 -> port 1, h2 -> port 2, h3 -> port 3
            out_port = None
            if src_mac == self.H1_MAC and dst_mac == self.H2_MAC:
                out_port = 2
            elif src_mac == self.H2_MAC and dst_mac == self.H1_MAC:
                out_port = 1

            if out_port is None:
                # Fallback: if unknown, try mac_to_port table
                out_port = self.mac_to_port[dpid].get(
                    dst_mac,
                    ofproto.OFPP_FLOOD
                )

            actions = [parser.OFPActionOutput(out_port)]

            # Install a flow for this specific traffic (match on IP src/dst)
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

            # Also send the current packet if not buffered
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                out = parser.OFPPacketOut(
                    datapath=datapath,
                    buffer_id=ofproto.OFP_NO_BUFFER,
                    in_port=in_port,
                    actions=actions,
                    data=msg.data
                )
                datapath.send_msg(out)

            self.logger.info("Permitted: %s -> %s via port %s",
                             src_ip, dst_ip, out_port)
            return

        # Case 2: destination is h3 (10.0.10.3) -> block (drop)
        if dst_ip == "10.0.10.3":
            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_dst=dst_ip
            )
            actions = []  # empty list => drop

            self.add_flow(
                datapath,
                priority=20,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id
                if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )

            self.logger.info("Blocking traffic towards %s (drop flow installed)",
                             dst_ip)
            # No packet-out is sent: the current packet is dropped.
            return

        # Default case: no action (log only)
        self.logger.info("Traffic not explicitly covered: %s -> %s (ignored)",
                         src_ip, dst_ip)
