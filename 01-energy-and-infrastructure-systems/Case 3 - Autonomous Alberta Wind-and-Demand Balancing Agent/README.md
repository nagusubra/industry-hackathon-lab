# Case 3 — Autonomous Alberta Wind-and-Demand Balancing Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Alberta now has a lot of wind. That is good — until a still, cold evening when people get home, the wind drops, and gas plants have to scramble. Those hours are when prices spike and the grid feels “tight.”

You are not being asked to run a full grid simulator. You are being asked to **spot the tight hours** from history: high demand, low wind, and (optional) Calgary weather that often goes with both.

**Your challenge:** Flag hours when Alberta load is high and wind is low. Recommend a simple action (hold a storage window, or ask a factory to wait). Beat “yesterday at the same hour” as a forecast. Then change your definition of “tight” once and show how many hours you would have warned.

---

## Industrial Significance

- AESO publishes hourly metered generation (including wind) and AIL. Calgary weather from ECCC is a free extra signal.
- **Who would use this:** a storage operator, a retailer, or an industrial load that can shift a few hours. **What is sold:** fewer surprise expensive hours; a one-page “tight evening” warning.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Hourly AIL, wind MW (and optional solar), from AESO. Optional: Calgary International hourly temperature / wind speed from ECCC.
2. **Reason:** Define a tightness score (example: AIL percentile high **and** wind percentile low). Keep the formula on one line.
3. **Act:** For a held-out week, output “tight / not tight” and a recommended window (e.g. “18:00–21:00, reduce load or pre-charge”).
4. **Iterate:** Loosen or tighten the percentile cut, re-score missed spikes vs false alarms.
5. **Explain:** How many tight hours, how they line up with high pool price (if you also load price from Case 1’s file).

Stretch: persistence baseline (same hour yesterday) vs a tiny sklearn model; do not overfit.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Score      │ -> │  Warn hours    │ -> │  Retune     │
│ AIL + wind  │    │ tight vs not │    │ vs persistence │    │ percentiles │
│ (+ weather) │    │              │    │                │    │             │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Persistence: yesterday’s same clock hour for load or for “tight” |
| Your flags | Precision/recall **or** a simple count of high-price hours caught vs missed (if price is loaded) |
| Loop | ≥ 1 threshold change after seeing false alarms |
| Demo | Plot of one week: AIL, wind, your flags |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
