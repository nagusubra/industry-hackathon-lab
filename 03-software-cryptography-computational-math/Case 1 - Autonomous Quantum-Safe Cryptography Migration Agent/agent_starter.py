#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous Quantum-Safe Cryptography Migration Agent
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import networkx as nx


NIST_MAP = {
    "RSA-2048": {"fips": "FIPS 203/204", "pqc": "ML-KEM-768 + ML-DSA-65", "priority": 1},
    "RSA-4096": {"fips": "FIPS 203/204", "pqc": "ML-KEM-1024 + ML-DSA-87", "priority": 1},
    "ECDSA-P256": {"fips": "FIPS 204", "pqc": "ML-DSA-65", "priority": 1},
    "ECDH-P256": {"fips": "FIPS 203", "pqc": "ML-KEM-768 (hybrid X25519+ML-KEM)", "priority": 1},
    "AES-256-GCM": {"fips": "symmetric OK", "pqc": "retain (increase key agility)", "priority": 3},
}


def write_sample_estate(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    estate = {
        "assets": [
            {"id": "api-gateway", "algo": "RSA-2048", "protocol": "TLS", "criticality": "high", "deps": ["hsm-1"]},
            {"id": "hsm-1", "algo": "ECDSA-P256", "protocol": "signing", "criticality": "critical", "deps": []},
            {"id": "iot-fleet", "algo": "ECDH-P256", "protocol": "MQTT-TLS", "criticality": "medium", "deps": ["api-gateway"]},
            {"id": "data-lake", "algo": "AES-256-GCM", "protocol": "at-rest", "criticality": "high", "deps": ["hsm-1"]},
            {"id": "legacy-vpn", "algo": "RSA-4096", "protocol": "IKE", "criticality": "high", "deps": ["api-gateway"]},
        ]
    }
    path.write_text(json.dumps(estate, indent=2), encoding="utf-8")
    print(f"[info] Wrote sample estate to {path}")


def perceive(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_graph(estate: dict[str, Any]) -> nx.DiGraph:
    g = nx.DiGraph()
    for asset in estate["assets"]:
        g.add_node(asset["id"], **asset)
        for dep in asset.get("deps", []):
            g.add_edge(asset["id"], dep)  # migrate dependencies first
    return g


def reason(g: nx.DiGraph) -> list[dict[str, Any]]:
    findings = []
    for node, data in g.nodes(data=True):
        algo = data.get("algo", "")
        mapping = NIST_MAP.get(algo, {"fips": "unknown", "pqc": "manual review", "priority": 2})
        findings.append({"id": node, "algo": algo, **mapping, "criticality": data.get("criticality")})
    findings.sort(key=lambda x: (x["priority"], 0 if x["criticality"] == "critical" else 1))
    return findings


def act(g: nx.DiGraph, findings: list[dict[str, Any]], budget_per_stage: int = 2) -> list[list[str]]:
    """Greedy wave planner: migrate dependency sinks first, then higher priority."""
    priority = {f["id"]: f["priority"] for f in findings}
    candidates = {n for n in g.nodes if priority.get(n, 99) <= 2}
    # Edges mean "depends on" → migrate successors (deps) before the node.
    if nx.is_directed_acyclic_graph(g):
        topo = list(reversed(list(nx.topological_sort(g))))
    else:
        topo = list(g.nodes)
    topo_index = {n: i for i, n in enumerate(topo)}

    stages: list[list[str]] = []
    migrated: set[str] = set()
    remaining = set(candidates)
    while remaining:
        ready = [
            n
            for n in remaining
            if set(g.successors(n)).issubset(migrated)
        ]
        if not ready:
            # Break cycles / missing deps by taking the earliest topo node
            ready = [min(remaining, key=lambda n: (priority.get(n, 99), topo_index.get(n, 10**9)))]
        ready.sort(key=lambda n: (priority.get(n, 99), topo_index.get(n, 10**9)))
        stage = ready[:budget_per_stage]
        stages.append(stage)
        migrated.update(stage)
        remaining -= set(stage)
    return stages


def evaluate(stages: list[list[str]], g: nx.DiGraph) -> dict[str, Any]:
    migrated: set[str] = set()
    violations = 0
    for stage in stages:
        for node in stage:
            deps = set(g.successors(node))
            if not deps.issubset(migrated):
                violations += 1
        migrated.update(stage)
    return {"n_stages": len(stages), "dependency_violations": violations, "coverage": len(migrated) / max(len(g), 1)}


def run_loop(estate_path: Path, iters: int = 3) -> None:
    estate = perceive(estate_path)
    g = build_graph(estate)
    findings = reason(g)
    budget = 2
    for i in range(1, iters + 1):
        stages = act(g, findings, budget_per_stage=budget)
        metrics = evaluate(stages, g)
        print(f"=== iteration {i} ===")
        print("findings:", json.dumps(findings, indent=2))
        print("stages:", stages)
        print("metrics:", metrics)
        # Autonomous repair: if violations, shrink stage size (stricter sequencing)
        if metrics["dependency_violations"] > 0 and budget > 1:
            budget -= 1
            print(f"[revise] reducing budget_per_stage -> {budget}")
        else:
            break
    print("TODO: integrate liboqs benchmarks and AutoPQC / PQC-MFB scorers.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 3 PQC migration starter agent")
    parser.add_argument(
        "--estate",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "sample_estate.json",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    if not args.estate.exists():
        write_sample_estate(args.estate)
    run_loop(args.estate, iters=args.iters)


if __name__ == "__main__":
    main()
