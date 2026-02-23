# Scenario SSH – simple provisioning

## Objective
Demonstrate SSH as a general-purpose control and automation mechanism.

## What happens
- A Python controller reads a JSON plan
- It connects via SSH
- It executes commands
- It transfers files

## What to observe
- SSH as a control protocol
- Multiple channels over a single connection
- Similarities with real DevOps tooling

## Run
docker compose up --build

## Discussion
- What makes SSH versatile
- Why many tools rely on SSH
