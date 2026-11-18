"""Feasibility and constant-space subnet selection regressions."""
import importlib.util
import ipaddress
from pathlib import Path
import random
import sys

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "subnet_quiz_generator.py"
SPEC = importlib.util.spec_from_file_location("course_subnet_quiz", SOURCE)
quiz = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = quiz
SPEC.loader.exec_module(quiz)


def test_seed20_and_deterministic_seed_sweep_are_feasible():
    for seed in range(1000):
        first = quiz.generate_vlsm_scenario(random.Random(seed))
        assert first == quiz.generate_vlsm_scenario(random.Random(seed))
        base, requirements, allocations = first
        assert [a.name for a in allocations] == [r.name for r in requirements]
        for i, allocation in enumerate(allocations):
            assert allocation.network.subnet_of(base)
            assert allocation.usable_hosts >= allocation.hosts_required
            assert all(not allocation.network.overlaps(other.network) for other in allocations[i + 1:])


def test_largest_pool_selection_uses_an_index_not_subnet_enumeration(monkeypatch):
    class FinalSubnet:
        def choice(self, options):
            return ipaddress.IPv4Network("10.0.0.0/8")
        def randint(self, low, high):
            return 30
        def randrange(self, count):
            assert count == 4194304
            return count - 1
    def forbidden(*args, **kwargs):
        raise AssertionError("Subnet enumeration must not occur")
    monkeypatch.setattr(ipaddress.IPv4Network, "subnets", forbidden)
    assert quiz._random_ipv4_network(FinalSubnet()) == ipaddress.IPv4Network("10.255.255.252/30")


@pytest.mark.parametrize("requirements", [[], [quiz.VlsmRequirement("A", 200), quiz.VlsmRequirement("B", 200)], [quiz.VlsmRequirement("A", 0)], [quiz.VlsmRequirement("A", 3), quiz.VlsmRequirement("A", 4)]])
def test_impossible_or_ambiguous_requirements_still_fail(requirements):
    with pytest.raises(ValueError):
        quiz.allocate_vlsm(ipaddress.IPv4Network("192.168.1.0/24"), requirements)
