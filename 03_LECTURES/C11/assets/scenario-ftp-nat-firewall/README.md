# Scenario FTP – NAT and firewall

## Objective
Demonstrate the limitations of FTP in modern networks that use NAT and firewalls.

## What happens
- The client communicates with the FTP server through a NAT device
- Active vs passive mode is tested
- Points of failure and their causes are observed

## What to observe
- Which side initiates the data connection
- Which ports are used
- Why passive mode is usually preferred

## Run
docker compose up --build

## Discussion
- Why FTP is difficult to secure
- Why SFTP and HTTPS are often preferred
