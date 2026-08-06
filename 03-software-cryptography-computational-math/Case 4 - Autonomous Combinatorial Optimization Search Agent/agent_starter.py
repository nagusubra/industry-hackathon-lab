#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous Combinatorial Optimization Search Agent
"""

from __future__ import annotations

import argparse
import json
import math
import random
from typing import Any

import numpy as np


def build_synthetic_tsp(n_cities: int = 8, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 100, size=(n_cities, 2))


def tour_length(coords: np.ndarray, tour: list[int]) -> float:
    total = 0.0
    for i in range(len(tour)):
        a, b = tour[i], tour[(i + 1) % len(tour)]
        total += math.hypot(coords[a, 0] - coords[b, 0], coords[a, 1] - coords[b, 1])
    return total


def perceive(coords: np.ndarray) -> dict[str, Any]:
    return {"problem": "TSP", "n_cities": len(coords), "bbox": coords.min(axis=0).tolist() + coords.max(axis=0).tolist()}


def nearest_neighbor(coords: np.ndarray, start: int = 0) -> list[int]:
    n = len(coords)
    unvisited = set(range(n)) - {start}
    tour = [start]
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: math.hypot(coords[current, 0] - coords[j, 0], coords[current, 1] - coords[j, 1]))
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    return tour


def two_opt(coords: np.ndarray, tour: list[int], max_passes: int = 50) -> tuple[list[int], list[dict[str, Any]]]:
    """Classic 2-opt local search; returns improved tour and improvement log."""
    n = len(tour)
    best = tour[:]
    best_len = tour_length(coords, best)
    history: list[dict[str, Any]] = [{"pass": 0, "length": round(best_len, 3)}]

    for p in range(1, max_passes + 1):
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                new_tour = best[:i] + best[i:j][::-1] + best[j:]
                new_len = tour_length(coords, new_tour)
                if new_len + 1e-9 < best_len:
                    best, best_len = new_tour, new_len
                    improved = True
        history.append({"pass": p, "length": round(best_len, 3)})
        if not improved:
            break
    return best, history


def reason(history: list[dict[str, Any]], window: int = 3) -> str:
    if len(history) < window + 1:
        return "continue_2opt"
    recent = [h["length"] for h in history[-window:]]
    if max(recent) - min(recent) < 0.01:
        return "restart"  # plateau — try new NN start
    return "continue_2opt"


def act(coords: np.ndarray, strategy: str, rng: random.Random) -> list[int]:
    if strategy == "restart":
        start = rng.randrange(len(coords))
        return nearest_neighbor(coords, start=start)
    return nearest_neighbor(coords)


def evaluate(initial_len: float, final_len: float) -> dict[str, Any]:
    gap = (final_len - initial_len) / max(initial_len, 1e-9)
    return {
        "initial_length": round(initial_len, 3),
        "final_length": round(final_len, 3),
        "improvement_pct": round(-100 * gap, 2),
    }


def run_loop(n_cities: int, iters: int, seed: int) -> None:
    coords = build_synthetic_tsp(n_cities=n_cities, seed=seed)
    summary = perceive(coords)
    print("instance:", json.dumps(summary, indent=2))

    rng = random.Random(seed)
    tour = act(coords, "restart", rng)
    initial_len = tour_length(coords, tour)

    best_tour = tour
    best_len = initial_len
    history: list[dict[str, Any]] = []

    for i in range(1, iters + 1):
        tour, opt_history = two_opt(coords, tour, max_passes=20)
        history.extend(opt_history)
        current_len = tour_length(coords, tour)
        if current_len < best_len:
            best_tour, best_len = tour, current_len

        strategy = reason(history)
        print(f"=== iteration {i} (strategy={strategy}) ===")
        print("tour:", best_tour)
        print("metrics:", evaluate(initial_len, best_len))

        if strategy == "restart":
            tour = act(coords, strategy, rng)
        else:
            tour = best_tour

    # Toy CVRP note
    print("CVRP toy: extend with capacity constraints and insertion heuristic.")
    print("TODO: load FrontierCO TSP/easy_test_instances; compare vs. bundled baselines.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 3 combinatorial optimization starter agent")
    parser.add_argument("--cities", type=int, default=8, help="Synthetic TSP city count")
    parser.add_argument("--iters", type=int, default=3, help="Agent revise loops")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run_loop(n_cities=args.cities, iters=args.iters, seed=args.seed)


if __name__ == "__main__":
    main()
