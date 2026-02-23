# Scenario FTP – control vs data

## Objective
Observe how FTP operates by inspecting the separation between:
- the control connection
- the data connection

## What happens
- A real FTP server runs (pyftpdlib)
- A Python FTP client connects
- LIST, STOR and RETR commands are executed
- Active vs passive mode is compared

## What to observe
- The ports in use
- When data connections appear
- The difference between PASV and PORT

## Run
docker compose up --build

## Questions
- Why do two separate connections exist?
- Why is active mode problematic?
