# Case 4 — Autonomous Transit-Fleet Remaining-Life Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Calgary Transit and City Fleet cannot wait for a bus or a truck to die on 17th Avenue. The honest problem is: **how many more trips before we pull this vehicle in?**

The City does not publish engine-sensor CSVs. NASA published a public jet-engine wear set that is the same *job* (readings over time → remaining life → inspect now vs later). You will practice on that open file and tell the story as a **fleet maintenance** tool.

**Your challenge:** Predict remaining useful life (how many cycles are left). Draw an “inspect this week” line. Count missed failures vs false alarms. **Move the line once** and show the new trade-off.

---

## Industrial Significance

- Unplanned downtime is expensive for Transit, Roads, and any Alberta trucking or oilfield fleet.
- **Who would use this:** Calgary Transit / Fleet Services (method), or a private shop. **What is sold:** fewer roadside failures without inspecting every vehicle every night.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load NASA C-MAPSS **FD001 only** (one operating condition, one fault mode). Columns: engine id, cycle, settings, sensors.
2. **Reason:** Compute remaining useful life on the training engines (last cycle = failure). A simple model is enough (linear model or random forest on a few sensors). No deep learning required.
3. **Act:** On the test set, predict RUL. Flag engines below a threshold as “inspect now.”
4. **Iterate:** Change the threshold; report missed failures vs extra inspections.
5. **Explain:** Which sensors mattered; what a shop would do with the list.

Stretch: compare to “use only the last cycle’s sensor 11” as a naive baseline.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Predict    │ -> │  Flag inspect  │ -> │  Move       │
│ FD001 train │    │ remaining    │    │ vs held-out    │    │ threshold   │
│ + test      │    │ cycles       │    │ RUL labels     │    │             │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md). Do **not** download FD002–FD004 for day one.

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| RUL error | MAE or RMSE on FD001 test engines vs NASA `RUL_FD001.txt` |
| Baseline | Persistence or a single-sensor linear trend — report both |
| Threshold | Precision/recall of “inspect now” after one revision |
| Loop | ≥ 1 threshold change |
| Scope | FD001 only |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
