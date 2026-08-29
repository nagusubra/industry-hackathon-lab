# Case 2 — Autonomous Bow-Elbow Water-Quality Flag Agent

**Stream:** Chemical Systems and Material Science  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Calgary drinks from the **Bow** and **Elbow**. The City already sends samples to an accredited lab. The remaining job is simple and high-stakes: **is this number over the limit, and which site should we resample?**

You are not being asked to invent new chemistry. You are being asked to compare lab results to a **small table of limits** and produce a red / yellow / green list.

**Your challenge:** Flag sites (or samples) that exceed a guideline. Beat “flag anything above the average.” Then **tighten or loosen one limit** and show how the list of red sites changes.

---

## Industrial Significance

- City of Calgary Water Quality Services publishes watershed monitoring (Bow, Elbow, Glenmore, Bearspaw) on DataStream. This is real compliance-style work.
- **Who would use this:** City water quality staff, or a consultant preparing a weekly exception report. **What is sold:** fewer missed exceedances and a list a manager can act on Monday morning.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load watershed sample rows (site, date, parameter, value, unit). Harmonize units if needed; drop rows you cannot interpret.
2. **Reason:** Join to a **limit table** (we list starter limits in the data guide; you may add CCME/Alberta citations). Flag over / near / under.
3. **Act:** Output a dashboard table: site, parameter, value, limit, status. Baseline = flag if value > column mean (a bad rule — show that it is noisy).
4. **Iterate:** Change one limit by ±20% (or switch to a stricter CCME number) and re-flag.
5. **Explain:** Which sites you would resample this week and why.

Do **not** recommend dumping chemicals or “treating the river.” Stay on monitoring and resampling.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Compare    │ -> │  Red/yellow    │ -> │  Change     │
│ lab CSV     │    │ to limits    │    │ vs mean-flag   │    │ one limit   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Flag if value > mean of that parameter (show why this is a weak rule) |
| Your flags | Count of exceedances vs baseline; list of sites |
| Loop | ≥ 1 limit sensitivity run |
| Safety | Monitoring / resample recommendations only |
| Demo | Table + one time-series plot for a single site |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
