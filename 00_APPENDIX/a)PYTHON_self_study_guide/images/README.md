# Screenshots Directory

Reserved directory for screenshots that accompany the Python self-study guide. Currently contains only the naming-convention specification; screenshot files will be added as the guide receives visual supplements.

| File | Description |
|---|---|
| [`README_SCREENSHOTS.md`](README_SCREENSHOTS.md) | Naming convention and contribution instructions for screenshot files |

## Naming Convention

```
[step]_[topic]_[description].png
```

Examples: `01_socket_server_terminal.png`, `02_wireshark_tcp_capture.png`, `03_portainer_dashboard.png`.

## Cross-References

Images placed here are referenced from [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) and the HTML presentations in [`../PRESENTATIONS_EN/`](../PRESENTATIONS_EN/).

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/images"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/images
```
