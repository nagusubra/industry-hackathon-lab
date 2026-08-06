# Case 4 — Autonomous Combinatorial Optimization Search Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Combinatorial optimization (TSP, CVRP, MIS, FJSP, etc.) underpins logistics, chip design, and network planning. **FrontierCO** provides standardized easy/hard instance splits with classical baselines — a rigorous testbed for search agents that must beat or match OR heuristics on unseen instances.

**Your challenge:** Build an **autonomous agent** that perceives problem instances, searches solution spaces (constructive + local search + learned policies), and iteratively improves objective values — beyond “ask an LLM for a tour.”

---

## Industrial Significance

- Last-mile routing (CVRP), facility location (CFLP), and network design (STP, MDS) are billion-dollar OR problems.
- FrontierCO unifies eight problem families with easy/hard splits for fair benchmarking against classical solvers.
- Agentic search loops (construct → evaluate → revise) mirror production OR pipelines in logistics and telecom.
- Alberta energy and agriculture logistics benefit from adaptive routing under real-world constraints.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load a FrontierCO instance (coordinates, demands, graph edges) for a chosen problem family.
2. **Construct:** Build an initial feasible solution (nearest neighbor, greedy, insertion heuristics).
3. **Search:** Apply local search (2-opt, swap, LNS) or metaheuristics / learned policies.
4. **Evaluate:** Compare tour length / objective vs. classical baselines on easy and hard splits.
5. **Iterate:** Agent switches neighborhoods or restarts when improvement stalls.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Instance parser -> Constructive heuristic -> Local search loop -> Objective evaluate -> Revise
```

**Starter frameworks (open source):**
- [FrontierCO dataset](https://huggingface.co/datasets/CO-Bench/FrontierCO) (MIT)
- [FrontierCO code](https://github.com/sunnweiwei/FrontierCO)
- Problems: CFLP, CPMP, CVRP, FJSP, MIS, MDS, STP, TSP
- Classical baselines bundled in the FrontierCO repository

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

| Metric | Target / Guidance |
|---|---|
| Optimality gap | ≤15% above best-known on TSP easy_test_instances |
| Search efficiency | Improvement within N iterations (report N) |
| Generalization | At least one additional problem family (e.g., CVRP) |
| Feasibility | 100% feasible solutions (capacity / precedence respected) |
| Autonomy | Neighborhood / restart policy adapts on plateau |
| Baseline comparison | Beat or match nearest-neighbor on held-out easy split |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
