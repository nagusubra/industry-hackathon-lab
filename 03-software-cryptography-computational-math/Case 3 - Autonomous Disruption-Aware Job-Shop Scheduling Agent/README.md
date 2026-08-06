# Case 3 — Autonomous Disruption-Aware Job-Shop Scheduling Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Job-shop scheduling (JSSP) assigns operations to machines to minimize makespan under precedence and capacity constraints. Real factories face **disruptions** — machine breakdowns, supply delays, rush orders — requiring fast reactive replanning, not a one-shot static schedule.

**Your challenge:** Build an **autonomous agent** that constructs an initial schedule, monitors disruption events, and iteratively replans while balancing makespan, tardiness, and stability — beyond “run a single OR-Tools solve.”

---

## Industrial Significance

- Manufacturing and energy logistics depend on robust scheduling under uncertainty; downtime costs thousands of dollars per hour.
- REALM-Bench provides standardized JSSP tiers (J1–J4) with scripted disruptions on classic Taillard/DMU/ABZ instances.
- Reactive replanning is a core operations-research + agentic-AI intersection: perceive state → reason about trade-offs → act → evaluate.
- Alberta industrial and supply-chain sectors need disruption-aware decision support, not static Gantt charts.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load a JSSP instance (jobs, machines, processing times) and disruption timeline from REALM-Bench.
2. **Plan:** Build an initial schedule (dispatching rules, CP-SAT, metaheuristics).
3. **React:** On disruption (machine down, job delay), revise the remaining schedule with minimal ripple.
4. **Evaluate:** Report makespan, tardiness, and schedule stability vs. static baseline.
5. **Iterate:** Agent adjusts dispatching policy or solver parameters when metrics degrade.

---

## Recommended Agent Architecture & Starter Code Pointers

```
JSSP instance -> Initial scheduler -> Disruption injector -> Replanner -> Metrics
```

**Starter frameworks (open source):**
- [REALM-Bench dataset](https://huggingface.co/datasets/GloriaGeng/REALM-Bench) (CC-BY-4.0)
- [REALM-Bench code](https://github.com/genglongling/REALM-Bench)
- Classic JSSP sources wrapped: Taillard, DMU, ABZ benchmarks
- Solvers: OR-Tools CP-SAT, custom dispatching rules, reinforcement learning baselines

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.**

---

## Success Criteria & Quantitative Evaluation Metrics

Report makespan (and tardiness if applicable) against concrete baselines — document what you compare against:

| Metric | Target / Guidance |
|---|---|
| Makespan vs. greedy baseline | Your scheduler vs. a fixed dispatching rule (FIFO, SPT) on J1 |
| Makespan vs. OR-Tools CP-SAT | If you use CP-SAT, report gap vs. optimal or best-known bound on J1 |
| Disruption recovery | Report makespan after replan vs. greedy baseline on J2; ≤20% increase vs. full replan-from-scratch is a **stretch goal** |
| Replan latency | Replan within seconds on J1/J2 instance sizes |
| Stability | Limit % of operations rescheduled (report metric) |
| Autonomy | Policy/solver params adapt after repeated disruptions |
| Tier progression | Demonstrate J1 → J2 before attempting J3/J4 |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
