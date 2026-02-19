# Scenario: MAC addresses, ARP and Ethernet basics

## Goal

This scenario links Layer 2 (Ethernet, MAC) to Layer 3 (IPv4) by observing how ARP resolves an IP address into a MAC address on a local network.

You will:

- Inspect your interface MAC address
- Generate ARP traffic by sending a ping
- Inspect the neighbour table (ARP cache)
- Capture ARP frames with `tcpdump` or Wireshark

## Requirements

- Linux (native, VM or container with capabilities)
- `iproute2` (for `ip`)
- Optional: `tcpdump` and/or Wireshark

## Steps

### 1) Identify your interface and MAC address

```bash
ip link
```

Pick an interface (e.g., `eth0`, `wlan0`) and inspect it:

```bash
ip link show dev eth0
```

You should see the `link/ether` field (the MAC address).

### 2) Inspect the neighbour table (ARP cache)

```bash
ip neigh
```

If the table is empty, this is fine.

### 3) Generate ARP traffic with ping

Pick a reachable host on your local network (often the gateway). For example:

```bash
ping -c 1 192.168.1.1
```

Now inspect the neighbour table again:

```bash
ip neigh
```

You should see an entry that maps the gateway IP to a MAC address.

### 4) Capture ARP frames

With `tcpdump` (replace interface as needed):

```bash
sudo tcpdump -i eth0 -n arp
```

In another terminal, repeat a ping or clear a neighbour entry and ping again:

```bash
sudo ip neigh flush all
ping -c 1 192.168.1.1
```

Observe the ARP request (broadcast) and ARP reply (unicast).

## Notes

- ARP is used only on the local L2 segment. Routers do not forward ARP broadcasts.
- In practice, ARP entries have timeouts and states (REACHABLE, STALE and others).

## Evidence (optional)

- A screenshot of `ip neigh` after a ping
- A short excerpt from `tcpdump` showing an ARP request and reply
