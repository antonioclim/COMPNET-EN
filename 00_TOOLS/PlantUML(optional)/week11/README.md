# Week 11 — FTP, DNS and SSH

7 PlantUML diagram sources for the application layer — FTP, DNS and SSH. Each file mirrors its counterpart in [`03_LECTURES/C11/assets/puml/`](../../../03_LECTURES/C11/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-dns-actors.puml` | Dns Actors | 40 |
| `fig-dns-resolution-overview.puml` | Dns Resolution Overview | 43 |
| `fig-dnssec-chain-of-trust.puml` | Dnssec Chain Of Trust | 44 |
| `fig-ftp-active-vs-passive.puml` | Ftp Active Vs Passive | 46 |
| `fig-ftp-control-data.puml` | Ftp Control Data | 52 |
| `fig-ssh-channels.puml` | Ssh Channels | 37 |
| `fig-ssh-port-forwarding.puml` | Ssh Port Forwarding | 51 |

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
| Lecture | [`03_LECTURES/C11/`](../../../03_LECTURES/C11/) |
| Seminar | [`04_SEMINARS/S11/`](../../../04_SEMINARS/S11/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week11"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week11
```
