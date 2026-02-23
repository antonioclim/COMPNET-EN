# Lectures

Thirteen lectures (C01–C13) cover the full span of computer networking, from physical-layer fundamentals through application protocols to IoT and security. Each lecture directory contains a slide-by-slide markdown file, PlantUML diagram sources in `assets/puml/`, rendered PNG images in `assets/images/` and executable demo scenarios in `assets/scenario-*/`.

## Lecture index

| Dir | Topic | File |
|-----|-------|------|
| C01 | Network fundamentals | `c1-network-fundamentals.md` |
| C02 | Architectural models (OSI and TCP/IP) | `c2-architectural-models.md` |
| C03 | Introduction to network programming | `c3-intro-network-programming.md` |
| C04 | Physical and data link layer | `c4-physical-and-data-link.md` |
| C05 | Network layer: addressing (IPv4, IPv6 and subnetting) | `c5-network-layer-addressing.md` |
| C06 | NAT, ARP, DHCP, NDP and ICMP | `c6-nat-arp-dhcp-ndp-icmp.md` |
| C07 | Routing protocols | `c7-routing-protocols.md` |
| C08 | Transport layer (TCP, UDP and TLS) | `c8-transport-layer.md` |
| C09 | Session and presentation layer | `c9-session-presentation.md` |
| C10 | Application layer: HTTP(S) | `c10-http-application-layer.md` |
| C11 | FTP, DNS and SSH | `c11-ftp-dns-ssh.md` |
| C12 | Email protocols (SMTP, POP3 and IMAP) | `c12-email-protocols.md` |
| C13 | IoT and network security | `c13-iot-security.md` |

## Generating diagrams

PNG files are generated from `.puml` sources. From any lecture directory run:

```
cd C01/assets && bash render.sh
```

The script requires Java and expects `plantuml.jar` to be present in `00_TOOLS/`.
If the JAR is absent, obtain it with:

```
bash 00_TOOLS/plantuml/get_plantuml_jar.sh
```

Regenerated PNGs are written to `assets/images/`.

## Scenarios

The `scenario-*` directories inside each lecture contain executable Python code that demonstrates the concepts covered in the slides. Some scenarios include a `docker-compose.yml` for containerised setups. Requirements: Python 3.10+ and Docker (optional).
