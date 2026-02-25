# Week 10 — HTTP(S), REST and WebSockets

10 PlantUML diagram sources for HTTP(S), REST and WebSockets. Each file mirrors its counterpart in [`03_LECTURES/C10/assets/puml/`](../../../03_LECTURES/C10/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-cors-preflight.puml` | Cors Preflight | 41 |
| `fig-http-caching-304.puml` | Http Caching 304 | 45 |
| `fig-http-methods-idempotency.puml` | Http Methods Idempotency | 35 |
| `fig-http-request-response.puml` | Http Request Response | 36 |
| `fig-http-reverse-proxy.puml` | Http Reverse Proxy | 44 |
| `fig-http11-vs-http2.puml` | Http11 Vs Http2 | 48 |
| `fig-https-tls-termination.puml` | Https Tls Termination | 53 |
| `fig-rest-maturity-levels.puml` | Rest Maturity Levels | 32 |
| `fig-websocket-upgrade-proxy.puml` | Websocket Upgrade Proxy | 37 |
| `fig-websocket-vs-polling.puml` | Websocket Vs Polling | 66 |

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
| Lecture | [`03_LECTURES/C10/`](../../../03_LECTURES/C10/) |
| Seminar | [`04_SEMINARS/S10/`](../../../04_SEMINARS/S10/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W10_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week10"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week10
```
