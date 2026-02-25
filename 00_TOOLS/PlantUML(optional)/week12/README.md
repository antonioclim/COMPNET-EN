# Week 12 — E-mail Protocols

10 PlantUML diagram sources for the application layer — e-mail (SMTP, POP3, IMAP). Each file mirrors its counterpart in [`03_LECTURES/C12/assets/puml/`](../../../03_LECTURES/C12/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-docker-mailstack.puml` | Docker Mailstack | 42 |
| `fig-email-security-layers.puml` | Email Security Layers | 40 |
| `fig-email-system.puml` | Email System | 53 |
| `fig-imap-session-states.puml` | Imap Session States | 37 |
| `fig-mime-multipart.puml` | Mime Multipart | 37 |
| `fig-pop3-session.puml` | Pop3 Session | 49 |
| `fig-pop3-vs-imap.puml` | Pop3 Vs Imap | 48 |
| `fig-smtp-envelope-vs-headers.puml` | Smtp Envelope Vs Headers | 37 |
| `fig-smtp-transaction.puml` | Smtp Transaction | 57 |
| `fig-webmail-architecture.puml` | Webmail Architecture | 36 |

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
| Lecture | [`03_LECTURES/C12/`](../../../03_LECTURES/C12/) |
| Seminar | [`04_SEMINARS/S12/`](../../../04_SEMINARS/S12/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W12_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W12_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week12"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week12
```
