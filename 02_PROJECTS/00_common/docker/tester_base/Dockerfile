# docker/tester_base/Dockerfile
# Base image for the "tester" (E2): runs pytest and captures PCAP
# RC2026 — use as a starting point in the student repository.

FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends tcpdump tshark ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# In the student repository copy requirements.txt (if present) and install dependencies.
# COPY requirements.txt /work/requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
