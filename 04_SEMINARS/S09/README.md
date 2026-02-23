# Seminar 09 — FTP, file transfer and containers

This seminar covers file transfer protocols: configuring pyftpdlib as a local FTP server, building a minimal custom file transfer server over sockets and testing multi-client scenarios inside Docker containers.

## Contents

Explanation files:

- `S09_Part01A_Explanation_File_Protocols_Intro.md` — overview of file transfer protocols
- `S09_Part01B_Explanation_Pyftpd.md` — pyftpdlib FTP server
- `S09_Part02A_Explanation_Pseudo_FTP.md` — custom file transfer implementation
- `S09_Part03A_Explanation_Multi_Client_Containers.md` — multi-client container setup

Task files:

- `S09_Part01E_Tasks_Pyftpd.md`
- `S09_Part02D_Tasks_Pseudo_FTP.md`
- `S09_Part03B_Tasks_Multi_Client_Containers.md`

The seminar includes 6 Python source files, 3 HTML support pages in `../_HTMLsupport/S09/` and 7 PlantUML diagrams in `assets/puml/`.

Docker Compose configuration for multi-client FTP testing is provided in `3_multi-client-containers/`.
