# Scenario DNS – TTL and caching

## Objective
Observe DNS caching behaviour and the operational effect of TTL.

## What happens
- A recursive resolver queries an authoritative server
- Responses are cached
- The DNS zone is modified

## What to observe
- When the new IP address becomes visible
- How TTL influences propagation

## Run
docker compose up --build

## Questions
- Why DNS changes are not instantaneous
- What trade-off TTL introduces
