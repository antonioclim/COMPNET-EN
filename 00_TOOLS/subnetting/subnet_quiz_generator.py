#!/usr/bin/env python3
"""
subnet_quiz_generator.py — dynamic subnetting quiz generator (optional)

The goal of this tool is *practice with immediate feedback*, not assessment.
It is intentionally self-contained (standard library only).

Modes
-----
- ipv4 : classic CIDR analysis questions (network/broadcast/hosts/netmask).
- vlsm : a compact scenario with host requirements and an answer key.

Examples
--------
Interactive IPv4 quiz:
  python3 subnet_quiz_generator.py --mode ipv4 --count 10

Markdown handout (+answers):
  python3 subnet_quiz_generator.py --mode ipv4 --count 10 --markdown quiz.md --show-answers

Single VLSM scenario:
  python3 subnet_quiz_generator.py --mode vlsm --seed 7 --show-answers
"""

from __future__ import annotations

import argparse
import ipaddress
import math
import random
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


PRIVATE_POOLS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
]


@dataclass(frozen=True)
class IPv4Question:
    network: ipaddress.IPv4Network
    prompt: str
    answer: str


def _random_ipv4_network(rng: random.Random) -> ipaddress.IPv4Network:
    """
    Generate a random private IPv4 network with a moderately sized prefix.

    Prefix range choice rationale:
    - /20 … /30 gives enough variety without producing huge address spaces
      that are tedious to reason about by hand.
    """
    pool = rng.choice(PRIVATE_POOLS)
    prefix = rng.randint(20, 30)

    # Pick a random *subnet* of the chosen pool with the chosen prefix.
    # We do this by selecting a random subnet index.
    subnets = list(pool.subnets(new_prefix=prefix))
    return rng.choice(subnets)


def _ipv4_netmask(prefix: int) -> str:
    return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)


def _usable_hosts(net: ipaddress.IPv4Network) -> int:
    # For /31 and /32, RFC semantics differ, but for teaching subnetting we use
    # the classic "network + broadcast not usable" model.
    if net.prefixlen >= 31:
        return 0
    return net.num_addresses - 2


def generate_ipv4_questions(rng: random.Random, count: int) -> List[IPv4Question]:
    questions: List[IPv4Question] = []

    for _ in range(count):
        net = _random_ipv4_network(rng)

        # Pick one question type at random.
        qtype = rng.choice(["network", "broadcast", "first", "last", "hosts", "netmask"])

        if qtype == "network":
            prompt = f"For {net.with_prefixlen}, what is the network address?"
            answer = str(net.network_address)
        elif qtype == "broadcast":
            prompt = f"For {net.with_prefixlen}, what is the broadcast address?"
            answer = str(net.broadcast_address)
        elif qtype == "first":
            first = net.network_address + 1 if net.prefixlen < 31 else net.network_address
            prompt = f"For {net.with_prefixlen}, what is the first usable host?"
            answer = str(first)
        elif qtype == "last":
            last = net.broadcast_address - 1 if net.prefixlen < 31 else net.broadcast_address
            prompt = f"For {net.with_prefixlen}, what is the last usable host?"
            answer = str(last)
        elif qtype == "hosts":
            prompt = f"For {net.with_prefixlen}, how many usable hosts exist?"
            answer = str(_usable_hosts(net))
        else:  # netmask
            prompt = f"For {net.with_prefixlen}, what is the netmask?"
            answer = _ipv4_netmask(net.prefixlen)

        questions.append(IPv4Question(network=net, prompt=prompt, answer=answer))

    return questions


@dataclass(frozen=True)
class VlsmRequirement:
    name: str
    hosts: int


@dataclass(frozen=True)
class VlsmAllocation:
    name: str
    hosts_required: int
    network: ipaddress.IPv4Network
    usable_hosts: int


def _smallest_prefix_for_hosts(hosts_required: int) -> int:
    """
    Return the smallest prefix that can accommodate hosts_required usable hosts.

    Classic model: usable hosts = 2^(hostbits) - 2
    -> hostbits = ceil(log2(hosts_required + 2))
    -> prefix   = 32 - hostbits
    """
    hostbits = math.ceil(math.log2(hosts_required + 2))
    prefix = 32 - hostbits
    # sanity clamp
    return max(0, min(32, prefix))


def allocate_vlsm(base: ipaddress.IPv4Network, reqs: List[VlsmRequirement]) -> List[VlsmAllocation]:
    """
    Greedy VLSM allocation: sort by descending host requirement, allocate sequentially.

    This matches the standard didactic approach:
    1) biggest subnet first
    2) align to boundary
    3) move to next free address
    """
    if not base.is_private:
        raise ValueError("Base network must be private for this generator.")

    # Sort by decreasing hosts.
    reqs_sorted = sorted(reqs, key=lambda r: r.hosts, reverse=True)

    allocations: List[VlsmAllocation] = []
    cursor = int(base.network_address)

    for r in reqs_sorted:
        prefix = _smallest_prefix_for_hosts(r.hosts)
        # Create a network starting from the cursor, but it must be aligned.
        candidate = ipaddress.IPv4Network((cursor, prefix), strict=False)
        if int(candidate.network_address) < cursor:
            # move to the next boundary if strict=False rounded down
            cursor = int(candidate.broadcast_address) + 1
            candidate = ipaddress.IPv4Network((cursor, prefix), strict=False)

        # Ensure candidate fits in base.
        if candidate.network_address < base.network_address or candidate.broadcast_address > base.broadcast_address:
            raise ValueError("VLSM allocation overflowed the base network. Increase base size.")

        allocations.append(
            VlsmAllocation(
                name=r.name,
                hosts_required=r.hosts,
                network=candidate,
                usable_hosts=_usable_hosts(candidate),
            )
        )
        cursor = int(candidate.broadcast_address) + 1

    # Return allocations in the original order (name order), for readability.
    # Note: we keep the greedy internal logic for correctness, but present results in a stable order.
    alloc_map = {a.name: a for a in allocations}
    return [alloc_map[r.name] for r in reqs]


def generate_vlsm_scenario(rng: random.Random) -> Tuple[ipaddress.IPv4Network, List[VlsmRequirement], List[VlsmAllocation]]:
    """
    Generate a small VLSM scenario: base /24 or /23 and 3–4 subnets.
    """
    base_pool = rng.choice(PRIVATE_POOLS)
    base_prefix = rng.choice([23, 24, 25])
    base = rng.choice(list(base_pool.subnets(new_prefix=base_prefix)))

    # 3–4 requirements; keep within plausible lab sizes.
    names = ["LAN_A", "LAN_B", "LAN_C", "DMZ"]
    rng.shuffle(names)
    reqs_count = rng.choice([3, 4])
    reqs: List[VlsmRequirement] = []
    for i in range(reqs_count):
        hosts = rng.choice([6, 10, 14, 20, 30, 50, 60, 100])
        reqs.append(VlsmRequirement(name=names[i], hosts=hosts))

    allocs = allocate_vlsm(base, reqs)
    return base, reqs, allocs


def normalise_answer(s: str) -> str:
    """
    Normalise user input for lenient comparison.
    - trim whitespace
    - allow '192.168.001.001' style variants by parsing as IPv4 where possible
    """
    s = s.strip()
    if not s:
        return s

    # For integer answers (host counts) keep digits only if possible.
    if s.isdigit():
        return s

    # For IPs and netmasks, ipaddress normalisation helps.
    try:
        return str(ipaddress.IPv4Address(s))
    except Exception:
        pass

    try:
        # netmask normalisation: accept prefix form too.
        if "/" in s:
            net = ipaddress.IPv4Network(s, strict=False)
            return str(net.netmask)
    except Exception:
        pass

    return s


def run_interactive_ipv4(questions: List[IPv4Question], show_answers: bool) -> None:
    correct = 0
    for i, q in enumerate(questions, start=1):
        print("-" * 72)
        print(f"Q{i}/{len(questions)}")
        print(q.prompt)
        user = input("Your answer: ").strip()

        user_n = normalise_answer(user)
        ans_n = normalise_answer(q.answer)

        if user_n == ans_n:
            print("✓ Correct")
            correct += 1
        else:
            print("✗ Not correct")
            if show_answers:
                print(f"  Expected: {q.answer}")

    print("=" * 72)
    print(f"Score: {correct}/{len(questions)} ({(100.0*correct/len(questions)):.1f}%)")
    print("=" * 72)


def render_markdown_ipv4(questions: List[IPv4Question], show_answers: bool) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: List[str] = []
    lines.append("# IPv4 Subnetting Quiz")
    lines.append("")
    lines.append(f"*Generated: {now}*")
    lines.append("")
    lines.append("## Questions")
    lines.append("")
    for i, q in enumerate(questions, start=1):
        lines.append(f"{i}. {q.prompt}")
    lines.append("")
    if show_answers:
        lines.append("## Answer key")
        lines.append("")
        for i, q in enumerate(questions, start=1):
            lines.append(f"{i}. **{q.answer}**")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown_vlsm(base: ipaddress.IPv4Network, reqs: List[VlsmRequirement], allocs: List[VlsmAllocation], show_answers: bool) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: List[str] = []
    lines.append("# VLSM Scenario (practice)")
    lines.append("")
    lines.append(f"*Generated: {now}*")
    lines.append("")
    lines.append(f"Base network: **{base.with_prefixlen}**")
    lines.append("")
    lines.append("## Requirements")
    lines.append("")
    for r in reqs:
        lines.append(f"- {r.name}: {r.hosts} usable hosts")
    lines.append("")
    lines.append("## Task")
    lines.append("")
    lines.append("Allocate subnets inside the base network using VLSM (largest first).")
    lines.append("")
    if show_answers:
        lines.append("## Answer key (one valid greedy allocation)")
        lines.append("")
        lines.append("| Segment | Hosts required | Allocated subnet | Usable hosts |")
        lines.append("|---|---:|---|---:|")
        for a in allocs:
            lines.append(f"| {a.name} | {a.hosts_required} | `{a.network.with_prefixlen}` | {a.usable_hosts} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Dynamic subnetting quiz generator (optional)")
    ap.add_argument("--mode", choices=["ipv4", "vlsm"], default="ipv4")
    ap.add_argument("--count", type=int, default=10, help="Number of IPv4 questions (mode=ipv4)")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    ap.add_argument("--show-answers", action="store_true", help="Reveal expected answers")
    ap.add_argument("--markdown", default=None, help="Write a Markdown quiz to this file (non-interactive)")
    args = ap.parse_args()

    rng = random.Random(args.seed)

    if args.mode == "ipv4":
        questions = generate_ipv4_questions(rng, max(1, args.count))
        if args.markdown:
            out = render_markdown_ipv4(questions, show_answers=args.show_answers)
            path = Path(args.markdown)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(out, encoding="utf-8")
            print(f"[OK] Wrote: {path}")
            return 0
        run_interactive_ipv4(questions, show_answers=args.show_answers)
        return 0

    # vlsm
    base, reqs, allocs = generate_vlsm_scenario(rng)
    md = render_markdown_vlsm(base, reqs, allocs, show_answers=args.show_answers)

    if args.markdown:
        path = Path(args.markdown)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md, encoding="utf-8")
        print(f"[OK] Wrote: {path}")
        return 0

    print(md)
    print("[TIP] Use --markdown out.md to generate a handout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
