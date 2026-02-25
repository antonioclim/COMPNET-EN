# Optional HTML Lecture Presentations

Fourteen self-contained HTML slide exports covering the full theory arc of the Computer Networks course, from network fundamentals (Week 1) through an integrated recap (Week 14). These were produced through an automated translation/export pipeline from Romanian originals and have been fully proofread as of February 2026.

The canonical, actively maintained lecture content resides in [`03_LECTURES/`](../../03_LECTURES/) as Markdown with figures and Docker scenarios. The HTML files here serve as a portable, browser-viewable alternative for students who prefer slides to structured Markdown.

## File Index

| File | Week | Topic | Format |
|---|---|---|---|
| [`S1Theory_Network_fundamentals_EN.html`](S1Theory_Network_fundamentals_EN.html) | 01 | Network fundamentals | HTML slides |
| [`S2Theory_Architectural_models_OSI_and_TCP_IP_EN.html`](S2Theory_Architectural_models_OSI_and_TCP_IP_EN.html) | 02 | OSI and TCP/IP models | HTML slides |
| [`S3Theory_UDP_Broadcast_Multicast_TCP_Tunnels_EN.html`](S3Theory_UDP_Broadcast_Multicast_TCP_Tunnels_EN.html) | 03 | UDP, broadcast, multicast, TCP tunnels | HTML slides |
| [`S4Theory_Physical_and_data_link_layer_EN.html`](S4Theory_Physical_and_data_link_layer_EN.html) | 04 | Physical and data link layer | HTML slides |
| [`S5Theory_Network_layer__IP_addressing_and_subnetting_EN.html`](S5Theory_Network_layer__IP_addressing_and_subnetting_EN.html) | 05 | Network layer, IP addressing, subnetting | HTML slides |
| [`S6Theory_NAT_PAT_ARP_DHCP_NDP_and_ICMP_EN.html`](S6Theory_NAT_PAT_ARP_DHCP_NDP_and_ICMP_EN.html) | 06 | NAT/PAT, ARP, DHCP, NDP, ICMP | HTML slides |
| [`S7Theory_Routing_protocols_EN.html`](S7Theory_Routing_protocols_EN.html) | 07 | Routing protocols | HTML slides |
| [`S8Theory_Transport_layer_EN.html`](S8Theory_Transport_layer_EN.html) | 08 | Transport layer | HTML slides |
| [`S9Theory_Session_and_presentation_concepts_EN.html`](S9Theory_Session_and_presentation_concepts_EN.html) | 09 | Session and presentation concepts | HTML slides |
| [`S10Theory_Application-layer_protocols_EN.html`](S10Theory_Application-layer_protocols_EN.html) | 10 | Application-layer protocols | HTML slides |
| [`S11Theory_FTP_DNS_and_SSH_EN.html`](S11Theory_FTP_DNS_and_SSH_EN.html) | 11 | FTP, DNS, SSH | HTML slides |
| [`S12Theory_Email_protocols_EN.html`](S12Theory_Email_protocols_EN.html) | 12 | Email protocols | HTML slides |
| [`S13Theory_IoT_and_network_security_EN.html`](S13Theory_IoT_and_network_security_EN.html) | 13 | IoT and network security | HTML slides |
| [`S14Theory_Integrated_RECAP_EN.html`](S14Theory_Integrated_RECAP_EN.html) | 14 | Integrated recap | HTML slides |

## Usage

Open any file directly in a browser — no server or build step is required:

```bash
xdg-open S1Theory_Network_fundamentals_EN.html    # Linux
open S1Theory_Network_fundamentals_EN.html          # macOS
start S1Theory_Network_fundamentals_EN.html         # Windows (PowerShell)
```

## Design Rationale

These exports exist as a convenience layer. If you intend to deliver directly from slides in a live teaching context, consider regenerating the HTML from an English source (Markdown + Reveal.js, Marp or Quarto) rather than patching the exported files.

## Cross-References — Lecture ↔ Seminar ↔ Quiz

| Week | HTML lecture (this folder) | Markdown lecture | Seminar | Quiz |
|---|---|---|---|---|
| 01 | `S1Theory…` | [`03_LECTURES/C01/`](../../03_LECTURES/C01/) | [`04_SEMINARS/S01/`](../../04_SEMINARS/S01/) | [`W01`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W01_Questions.md) |
| 02 | `S2Theory…` | [`03_LECTURES/C02/`](../../03_LECTURES/C02/) | [`04_SEMINARS/S02/`](../../04_SEMINARS/S02/) | [`W02`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W02_Questions.md) |
| 03 | `S3Theory…` | [`03_LECTURES/C03/`](../../03_LECTURES/C03/) | [`04_SEMINARS/S03/`](../../04_SEMINARS/S03/) | [`W03`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md) |
| 04 | `S4Theory…` | [`03_LECTURES/C04/`](../../03_LECTURES/C04/) | [`04_SEMINARS/S04/`](../../04_SEMINARS/S04/) | [`W04`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W04_Questions.md) |
| 05 | `S5Theory…` | [`03_LECTURES/C05/`](../../03_LECTURES/C05/) | [`04_SEMINARS/S05/`](../../04_SEMINARS/S05/) | [`W05`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md) |
| 06 | `S6Theory…` | [`03_LECTURES/C06/`](../../03_LECTURES/C06/) | [`04_SEMINARS/S06/`](../../04_SEMINARS/S06/) | [`W06`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md) |
| 07 | `S7Theory…` | [`03_LECTURES/C07/`](../../03_LECTURES/C07/) | [`04_SEMINARS/S07/`](../../04_SEMINARS/S07/) | [`W07`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W07_Questions.md) |
| 08 | `S8Theory…` | [`03_LECTURES/C08/`](../../03_LECTURES/C08/) | [`04_SEMINARS/S08/`](../../04_SEMINARS/S08/) | [`W08`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md) |
| 09 | `S9Theory…` | [`03_LECTURES/C09/`](../../03_LECTURES/C09/) | — | [`W09`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W09_Questions.md) |
| 10 | `S10Theory…` | [`03_LECTURES/C10/`](../../03_LECTURES/C10/) | [`04_SEMINARS/S09/`](../../04_SEMINARS/S09/) | [`W10`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md) |
| 11 | `S11Theory…` | [`03_LECTURES/C11/`](../../03_LECTURES/C11/) | [`04_SEMINARS/S10/`](../../04_SEMINARS/S10/) | [`W11`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md) |
| 12 | `S12Theory…` | [`03_LECTURES/C12/`](../../03_LECTURES/C12/) | [`04_SEMINARS/S11/`](../../04_SEMINARS/S11/) | [`W12`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W12_Questions.md) |
| 13 | `S13Theory…` | [`03_LECTURES/C13/`](../../03_LECTURES/C13/) | [`04_SEMINARS/S12/`](../../04_SEMINARS/S12/) | [`W13`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W13_Questions.md) |
| 14 | `S14Theory…` | [`03_LECTURES/C14/`](../../03_LECTURES/C14/) | [`04_SEMINARS/S13/`](../../04_SEMINARS/S13/) | [`W14`](../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W14_Questions.md) |

### Downstream Dependencies

No other repository components reference these HTML files directly. They are standalone reading material.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/b)optional_LECTURES"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/b)optional_LECTURES
```

---

*Optional HTML lectures — Computer Networks, ASE Bucharest, CSIE*
*Author: ing. dr. Antonio Clim — February 2026 (fully proofread)*
