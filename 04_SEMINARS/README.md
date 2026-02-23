# Seminars

Thirteen practical seminars (S01–S13) progress from basic network analysis through socket programming and protocol implementation to security testing and RPC frameworks. Each seminar directory contains markdown files (Explanation, Tasks and Scenario), Python source code, Docker configurations where applicable and PlantUML diagrams.

## Seminar index

| Dir | Topic |
|-----|-------|
| S01 | Network analysis: Wireshark/tshark, netcat (TCP/UDP) and traffic debugging |
| S02 | Socket programming: concurrent TCP and UDP server with clients and traffic analysis |
| S03 | UDP broadcast, multicast and a TCP tunnel |
| S04 | Custom text and binary protocols over TCP and UDP |
| S05 | IPv4/IPv6 subnetting and network simulation |
| S06 | SDN: simulated topologies and traffic analysis |
| S07 | Packet capture: packet filter and port scanning |
| S08 | HTTP server implementation and reverse proxies |
| S09 | File protocols: FTP server, minimal file transfer and multi-client containers |
| S10 | DNS, SSH and FTP in Docker containers |
| S11 | Load balancing and reverse proxying with Nginx and Docker Compose |
| S12 | Remote method invocation: JSON-RPC, Protobuf and gRPC |
| S13 | Network security: port scanning and vulnerability testing |

## Supporting materials

`_HTMLsupport/` contains HTML versions of the seminar materials for direct browser viewing. Each `S{NN}/` subfolder maps to the corresponding seminar directory.

`_tutorial-solve/` contains reference solutions. Solutions are currently available for S01 and S02; the rest are being added incrementally.

## Diagrams

Each seminar has `assets/puml/` with PlantUML sources and `assets/render.sh` for PNG generation. The render script requires Java and `plantuml.jar` in `00_TOOLS/`. Regenerated PNGs are written to `assets/images/`.
