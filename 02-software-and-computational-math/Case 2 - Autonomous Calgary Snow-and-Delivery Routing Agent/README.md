# Case 2 — Autonomous Calgary Snow-and-Delivery Routing Agent

**Stream:** Software and Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

After a storm, Calgary cannot treat every street at once. Snow-and-ice control has **priority routes**. The same math is a courier with 20 stops: you need an order that is short, and you need to **improve it once** when a road closes or a stop is added.

You will not solve Calgary’s entire plow network. You will route **about 15–25 stops**.

**Your challenge:** Build a tour (or a capacity-limited route) for a small set of Calgary points. Beat nearest-neighbour. Then swap two stops (or drop one blocked stop) and show the new distance.

---

## Industrial Significance

- City of Calgary Roads publishes snow-and-ice priority routes. Couriers and Waste & Recycling run the same “short tour” problem every day.
- **Who would use this:** Roads SNIC planners, or a local delivery firm. **What is sold:** fewer kilometres and a plan that can change when a street is impassable.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load 15–25 stop coordinates (community centroids, a sample of snow-priority vertices, or a table you build from Open Calgary). Compute a distance matrix (haversine km is enough).
2. **Reason:** Nearest-neighbour tour from a depot (e.g. downtown or a City yard you pick).
3. **Act:** Improve with one **2-opt** or pairwise swap. Report km before and after.
4. **Iterate:** Remove one stop (“road closed”) or add a high-priority stop; rebuild from the last tour instead of from scratch if you can.
5. **Explain:** Map or ordered list; km saved vs nearest-neighbour.

Stretch: two trucks with a simple capacity; snow priority class must be visited before residential samples.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   NN tour    │ -> │  2-opt / swap  │ -> │  Road closed│
│ 15–25 stops │    │ (baseline)   │    │  shorter km    │    │  replan     │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md). Do not ingest full Calgary Transit `stop_times.txt` (~60 MB) for day one.

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Nearest-neighbour from a stated depot |
| Improvement | Lower total km after 2-opt/swap (report both numbers) |
| Disruption | One closed stop or extra stop; new tour |
| Feasibility | Visit each stop once (TSP) or respect a simple capacity (CVRP stretch) |
| Loop | ≥ 1 improve **and** ≥ 1 disruption |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
