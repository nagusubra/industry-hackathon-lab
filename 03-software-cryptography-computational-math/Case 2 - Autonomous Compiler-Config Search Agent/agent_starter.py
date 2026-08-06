#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous Compiler-Config Search Agent
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np


@dataclass
class CompilerConfig:
    tile_m: int
    tile_n: int
    tile_k: int
    layout: str  # "row" | "col"

    def as_vector(self) -> list[int | str]:
        return [self.tile_m, self.tile_n, self.tile_k, self.layout]

    @classmethod
    def random(cls, rng: random.Random) -> CompilerConfig:
        return cls(
            tile_m=rng.choice([8, 16, 32, 64]),
            tile_n=rng.choice([8, 16, 32, 64]),
            tile_k=rng.choice([8, 16, 32]),
            layout=rng.choice(["row", "col"]),
        )


def build_synthetic_graph(seed: int = 42) -> nx.DiGraph:
    """Small matmul-heavy graph mimicking an XLA subgraph."""
    rng = random.Random(seed)
    g = nx.DiGraph()
    ops = ["param", "matmul", "relu", "matmul", "add", "softmax"]
    for i, op in enumerate(ops):
        g.add_node(i, op=op, flops=rng.randint(1_000, 50_000))
        if i > 0:
            g.add_edge(i - 1, i)
    return g


def perceive(g: nx.DiGraph) -> dict[str, Any]:
    total_flops = sum(d.get("flops", 0) for _, d in g.nodes(data=True))
    return {
        "n_nodes": g.number_of_nodes(),
        "n_edges": g.number_of_edges(),
        "ops": [d["op"] for _, d in g.nodes(data=True)],
        "total_flops": total_flops,
    }


def runtime_oracle(g: nx.DiGraph, config: CompilerConfig, seed: int = 0) -> float:
    """
    Synthetic config→runtime oracle (lower is better).
    Hidden optimum near tile 32×32×16, row layout.
    """
    cfg_key = (config.tile_m, config.tile_n, config.tile_k, config.layout)
    rng = np.random.default_rng(seed + hash(cfg_key) % 10_000)
    total_flops = sum(d.get("flops", 0) for _, d in g.nodes(data=True))
    tile_penalty = abs(config.tile_m - 32) + abs(config.tile_n - 32) + abs(config.tile_k - 16)
    layout_penalty = 0 if config.layout == "row" else 12.0
    noise = float(rng.normal(0, 2.0))
    return total_flops / 10_000 + tile_penalty * 0.8 + layout_penalty + noise


def random_search(
    g: nx.DiGraph,
    n_trials: int,
    seed: int,
) -> tuple[CompilerConfig, float, list[dict[str, Any]]]:
    rng = random.Random(seed)
    history: list[dict[str, Any]] = []
    best_cfg = CompilerConfig(16, 16, 8, "col")
    best_rt = float("inf")
    for t in range(1, n_trials + 1):
        cfg = CompilerConfig.random(rng)
        rt = runtime_oracle(g, cfg, seed=seed + t)
        history.append({"trial": t, "config": cfg.as_vector(), "runtime_ms": rt})
        if rt < best_rt:
            best_rt, best_cfg = rt, cfg
    return best_cfg, best_rt, history


def reason(history: list[dict[str, Any]], plateau_window: int = 5) -> str:
    if len(history) < plateau_window:
        return "explore"
    recent = [h["runtime_ms"] for h in history[-plateau_window:]]
    if max(recent) - min(recent) < 1.0:
        return "intensify"  # plateau — mutate around best
    return "explore"


def act(
    g: nx.DiGraph,
    best_cfg: CompilerConfig,
    strategy: str,
    rng: random.Random,
) -> CompilerConfig:
    if strategy == "intensify":
        return CompilerConfig(
            tile_m=max(8, min(64, best_cfg.tile_m + rng.choice([-8, 0, 8]))),
            tile_n=max(8, min(64, best_cfg.tile_n + rng.choice([-8, 0, 8]))),
            tile_k=max(8, min(32, best_cfg.tile_k + rng.choice([-8, 0, 8]))),
            layout=best_cfg.layout,
        )
    return CompilerConfig.random(rng)


def evaluate(best_rt: float, baseline_rt: float) -> dict[str, Any]:
    improvement = (baseline_rt - best_rt) / max(baseline_rt, 1e-9)
    return {
        "best_runtime_ms": round(best_rt, 3),
        "baseline_runtime_ms": round(baseline_rt, 3),
        "improvement_pct": round(100 * improvement, 2),
    }


def run_loop(n_trials: int, iters: int, seed: int) -> None:
    g = build_synthetic_graph(seed=seed)
    summary = perceive(g)
    print("graph:", json.dumps(summary, indent=2))

    rng = random.Random(seed)
    _, baseline_rt, _ = random_search(g, n_trials=3, seed=seed)

    best_cfg = CompilerConfig(16, 16, 8, "col")
    best_rt = float("inf")
    history: list[dict[str, Any]] = []

    per_iter = max(1, n_trials // iters)
    for i in range(1, iters + 1):
        strategy = reason(history)
        for _ in range(per_iter):
            cfg = act(g, best_cfg, strategy, rng)
            rt = runtime_oracle(g, cfg, seed=seed + len(history))
            history.append({"trial": len(history) + 1, "config": cfg.as_vector(), "runtime_ms": rt})
            if rt < best_rt:
                best_rt, best_cfg = rt, cfg
        metrics = evaluate(best_rt, baseline_rt)
        print(f"=== iteration {i} (strategy={strategy}) ===")
        print("best_config:", best_cfg.as_vector())
        print("metrics:", metrics)

    print("TODO: swap oracle for TpuGraphs measured runtimes; integrate Nevergrad / Optuna search.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 3 compiler-config search starter agent")
    parser.add_argument("--trials", type=int, default=30, help="Total config evaluations")
    parser.add_argument("--iters", type=int, default=3, help="Agent revise loops")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run_loop(n_trials=args.trials, iters=args.iters, seed=args.seed)


if __name__ == "__main__":
    main()
