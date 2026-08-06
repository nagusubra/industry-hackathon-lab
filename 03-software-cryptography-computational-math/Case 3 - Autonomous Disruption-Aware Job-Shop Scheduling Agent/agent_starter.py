#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous Disruption-Aware Job-Shop Scheduling Agent
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Operation:
    job: int
    op_idx: int
    machine: int
    duration: int
    start: int = 0
    end: int = 0


@dataclass
class JSSPInstance:
    """Synthetic 3-job × 3-machine JSSP."""
    jobs: list[list[tuple[int, int]]] = field(default_factory=list)  # (machine, duration) per op

    @classmethod
    def synthetic(cls) -> JSSPInstance:
        return cls(
            jobs=[
                [(0, 3), (1, 2), (2, 2)],
                [(0, 2), (2, 1), (1, 4)],
                [(1, 4), (0, 3), (2, 2)],
            ]
        )


@dataclass
class Disruption:
    time: int
    machine: int
    duration: int
    kind: str = "breakdown"


def perceive(instance: JSSPInstance) -> dict[str, Any]:
    n_ops = sum(len(job) for job in instance.jobs)
    return {
        "n_jobs": len(instance.jobs),
        "n_machines": max(m for job in instance.jobs for m, _ in job) + 1,
        "n_operations": n_ops,
    }


def greedy_schedule(
    instance: JSSPInstance,
    disruptions: list[Disruption] | None = None,
    priority: str = "spt",
    rng: random.Random | None = None,
) -> list[Operation]:
    """
    Greedy list scheduling: per job, schedule next op when machine + predecessor free.
    priority: 'spt' (shortest processing time) or 'fifo'.
    """
    disruptions = disruptions or []
    machine_free = [0, 0, 0]
    job_next: list[int] = [0] * len(instance.jobs)
    job_end: list[int] = [0] * len(instance.jobs)
    scheduled: list[Operation] = []

    def machine_blocked(machine: int, t: int) -> int:
        """Return earliest time >= t when machine is available."""
        for d in disruptions:
            if d.machine == machine and d.time <= t < d.time + d.duration:
                t = d.time + d.duration
        return t

    total_ops = sum(len(j) for j in instance.jobs)
    while len(scheduled) < total_ops:
        candidates: list[Operation] = []
        for j, job in enumerate(instance.jobs):
            k = job_next[j]
            if k >= len(job):
                continue
            machine, duration = job[k]
            est = max(job_end[j], machine_free[machine])
            est = machine_blocked(machine, est)
            candidates.append(Operation(j, k, machine, duration, start=est, end=est + duration))

        if priority == "spt":
            candidates.sort(key=lambda o: (o.duration, o.job, rng.random() if rng else 0))
        else:
            candidates.sort(key=lambda o: (o.job, o.op_idx, rng.random() if rng else 0))

        op = candidates[0]
        machine_free[op.machine] = op.end
        job_end[op.job] = op.end
        job_next[op.job] += 1
        scheduled.append(op)

    return scheduled


def inject_disruption(time: int = 5) -> Disruption:
    return Disruption(time=time, machine=0, duration=4, kind="breakdown")


def evaluate(schedule: list[Operation]) -> dict[str, Any]:
    makespan = max(op.end for op in schedule) if schedule else 0
    return {"makespan": makespan, "n_operations": len(schedule)}


def reason(static_makespan: int, disrupted_makespan: int) -> str:
    delta = disrupted_makespan - static_makespan
    if delta > 3:
        return "tighten"  # switch to SPT for shorter jobs first
    return "fifo"


def run_loop(seed: int = 42) -> None:
    rng = random.Random(seed)
    instance = JSSPInstance.synthetic()
    summary = perceive(instance)
    print("instance:", json.dumps(summary, indent=2))

    static = greedy_schedule(instance, priority="fifo", rng=rng)
    static_metrics = evaluate(static)
    print("=== static schedule (no disruption) ===")
    print("schedule:", [(o.job, o.op_idx, o.machine, o.start, o.end) for o in static])
    print("metrics:", static_metrics)

    disruption = inject_disruption(time=5)
    print(f"=== disruption injected: {disruption} ===")

    disrupted = greedy_schedule(instance, disruptions=[disruption], priority="fifo", rng=rng)
    disrupted_metrics = evaluate(disrupted)
    print("disrupted schedule (fifo):", disrupted_metrics)

    strategy = reason(static_metrics["makespan"], disrupted_metrics["makespan"])
    replanned = greedy_schedule(
        instance,
        disruptions=[disruption],
        priority="spt" if strategy == "tighten" else "fifo",
        rng=rng,
    )
    replanned_metrics = evaluate(replanned)
    print(f"=== replan iteration (strategy={strategy}) ===")
    print("replanned schedule:", [(o.job, o.op_idx, o.machine, o.start, o.end) for o in replanned])
    print("metrics:", replanned_metrics)

    print("TODO: load REALM-Bench J1/J2; integrate OR-Tools CP-SAT replanner.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 3 JSSP disruption-aware starter agent")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run_loop(seed=args.seed)


if __name__ == "__main__":
    main()
