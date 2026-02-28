# C14 — Week 14 integration lab (capstone)

## Purpose

This lab is designed as a capstone integration exercise that consolidates:

- DNS authority and caching behaviour
- HTTP reverse proxy routing and rewriting
- Forwarded headers and trust boundaries
- TLS termination (optional extension)

It is intentionally structured so students can narrate a complete request path end-to-end.

## Lab artefact

Use the Docker Compose scenario:

- `03_LECTURES/C14/assets/scenario-week14-integration-lab/`

## Learning outcomes

By the end of the lab, a student should be able to:

1. Explain the difference between an authoritative name server and a caching recursive resolver.
2. Demonstrate TTL behaviour and relate it to caching.
3. Explain reverse proxy responsibilities (routing, rewriting, redirects).
4. Explain and validate `X-Forwarded-*` headers.
5. (Extension) Explain TLS termination and where plaintext traffic exists.

## Deliverables

A short technical report or lab worksheet containing:

- A diagram of the request path (DNS + HTTP), with component names.
- Evidence screenshots/logs for:
  - authoritative vs resolver DNS answers
  - HTTP redirect and rewrite behaviour
  - `/api/users` response showing forwarded headers
- A concise explanation (≤ 200 words each) for:
  - why forwarded headers are a trust boundary
  - what changes when TLS termination is enabled

## Marking rubric (example)

- **Correctness** (50%): evidence matches claims; protocol layering is correct.
- **Clarity** (30%): diagrams and explanations are readable and technically precise.
- **Extension** (20%): TLS variant and/or proxy hardening (rate limit/caching).

## Suggested extensions

- Add Nginx rate limiting for `/api/`.
- Add proxy caching for `/api/users`.
- Capture a pcap and annotate DNS + HTTP (and TLS handshake in the variant).

