# Case 1 — Autonomous 311 Work-Order Dispatch Agent

**Stream:** Software and Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Calgary 311 is a pile of potholes, ice, garbage, signs, and “other.” If every crew takes the **oldest ticket**, a safety issue sits behind a backlog of small complaints. Then a blizzard hits — or a crew calls in sick — and the plan you made at 7 a.m. is wrong.

This is a **tiny job shop** in City clothes: jobs (tickets), machines (crews), and a disruption.

**Your challenge:** Score open tickets and assign them to a small number of crews for one day. Beat first-come-first-served. Then apply one disruption (blizzard: ice/snow tickets jump in priority, **or** one crew disappears) and **reassign**. Report how many jobs moved.

---

## Industrial Significance

- 311 / Roads / Waste & Recycling already live in this world. A dispatcher’s job is priority + geography + who is available.
- **Who would use this:** 311 operations, Roads, Waste & Recycling. **What is sold:** more of the *right* work done when capacity drops.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load 311 (current year is enough). Filter to a handful of service types (e.g. potholes, snow/ice, waste). Keep community and dates.
2. **Reason:** Give each ticket a priority score (age, service type, maybe community). Assign up to `C` crews × `K` jobs each (you pick `C` and `K`).
3. **Act:** Produce a day plan. Baseline = oldest tickets first, ignore type.
4. **Iterate:** Disruption. Replan. Measure: jobs completed proxy, and % of jobs that changed crew or slot.
5. **Explain:** What you would tell the supervisor at 8 a.m. and at noon.

Keep geography simple: optional “same community preferred” bonus — do not build a full GIS router here (that is Case 2).

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Prioritize │ -> │  Assign crews  │ -> │  Disrupt    │
│ 311 subset  │    │ vs FIFO      │    │ day plan       │    │ and replan  │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | FIFO (oldest first) for the same crew capacity |
| Your plan | Higher total priority points (your score) than FIFO, or same points with better safety-type coverage |
| Disruption | Replan in code; report % jobs moved |
| Loop | ≥ 1 disruption cycle |
| Size | Use a **sample** of tickets (e.g. 80–200), not the full 311 history |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
