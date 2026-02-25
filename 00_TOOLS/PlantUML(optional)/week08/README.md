# Week 08 — Transport Layer

12 PlantUML diagram sources for the transport layer — TCP, UDP, TLS and QUIC. Each file mirrors its counterpart in [`03_LECTURES/C08/assets/puml/`](../../../03_LECTURES/C08/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-diffie-hellman.puml` | Diffie Hellman | 57 |
| `fig-quic-handshake.puml` | Quic Handshake | 41 |
| `fig-tcp-close.puml` | Tcp Close | 44 |
| `fig-tcp-handshake.puml` | Tcp Handshake | 39 |
| `fig-tcp-header.puml` | Tcp Header | 47 |
| `fig-tcp-sack.puml` | Tcp Sack | 41 |
| `fig-tcp-states.puml` | Tcp States | 54 |
| `fig-tcp-vs-udp.puml` | Tcp Vs Udp | 38 |
| `fig-tls-13.puml` | Tls 13 | 41 |
| `fig-tls-stack.puml` | Tls Stack | 35 |
| `fig-udp-header.puml` | Udp Header | 33 |
| `fig-udp-vs-tcp-loss-topo.puml` | Udp Vs Tcp Loss Topo | 43 |

## Usage

Render all diagrams in this directory with the local JAR:

```bash
java -jar ../../../00_TOOLS/plantuml.jar -tpng *.puml
```

Or via the HTTP server:

```bash
cd .. && python3 generate_png_simple.py
```

## Cross-References

| Aspect | Link |
|---|---|
| Lecture | [`03_LECTURES/C08/`](../../../03_LECTURES/C08/) |
| Seminar | [`04_SEMINARS/S08/`](../../../04_SEMINARS/S08/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W08_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week08"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week08
```
