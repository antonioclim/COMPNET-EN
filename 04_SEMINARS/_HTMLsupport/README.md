# _HTMLsupport — Browser-Viewable HTML Renderings

This directory contains HTML versions of the seminar materials, organised by seminar number. Each HTML page mirrors the corresponding Markdown explanation, scenario or Python source from the parent seminar directory, rendered for direct viewing in a web browser without requiring a Markdown renderer or IDE.

## Folder Index

| Directory | Corresponding Seminar | HTML Files |
|---|---|---|
| [`S01/`](S01/) | [`../S01/`](../S01/) — Wireshark, netcat and traffic debugging | 2 |
| [`S02/`](S02/) | [`../S02/`](../S02/) — TCP and UDP socket programming | 11 |
| [`S03/`](S03/) | [`../S03/`](../S03/) — Broadcast, multicast and multi-client TCP | 6 |
| [`S04/`](S04/) | [`../S04/`](../S04/) — Custom text and binary protocols | 3 |
| [`S05/`](S05/) | [`../S05/`](../S05/) — IPv4/IPv6 subnetting and simulation | 4 |
| [`S06/`](S06/) | [`../S06/`](../S06/) — SDN, routing and Mininet topologies | 4 |
| [`S07/`](S07/) | [`../S07/`](../S07/) — Sniffing, filtering, scanning and IDS | 6 |
| [`S08/`](S08/) | [`../S08/`](../S08/) — HTTP server and Nginx reverse proxy | 5 |
| [`S09/`](S09/) | [`../S09/`](../S09/) — FTP, file transfer and containers | 3 |
| [`S10/`](S10/) | [`../S10/`](../S10/) — DNS, SSH and port forwarding in Docker | 5 |
| [`S11/`](S11/) | [`../S11/`](../S11/) — Load balancing with Nginx and custom balancer | 8 |
| [`S12/`](S12/) | [`../S12/`](../S12/) — JSON-RPC, Protobuf and gRPC | 3 |
| [`S13/`](S13/) | [`../S13/`](../S13/) — Penetration testing | 1 |

S14 does not have an HTML rendering at present.

## Usage

Open any `.html` file directly in a browser:

```bash
xdg-open S01/S01_Part01_Page_CLI_Netcat_Wireshark_Sim.html
```

Or serve the directory locally:

```bash
python3 -m http.server 8080 --directory .
```

## Pedagogical Context

HTML renderings serve students who prefer browser-based reading or who do not have a Markdown-capable editor. They also support offline use in lab environments where GitHub may be unavailable.

## Cross-References

The authoritative source for each HTML page is the corresponding Markdown or Python file in [`../S01/`](../S01/) through [`../S13/`](../S13/). If content diverges, the Markdown source is canonical.

No other repository components depend on this directory. Removing it would not break any cross-references or CI pipelines.

## Selective Clone

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 04_SEMINARS/_HTMLsupport
```

**Method B — Direct download**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/04_SEMINARS/_HTMLsupport
```

---

*Course: COMPNET-EN — ASE Bucharest, CSIE*
