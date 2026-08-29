# Case 5 — Autonomous Calgary Collision-Hotspot Ranking Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Some Calgary corners show up in crash reports again and again. Roads has a **limited safety budget**. Ranking by “most crashes” alone can hide a quieter intersection where crashes are getting *worse*, or where injuries are more serious.

**Your challenge:** From open traffic-incident records, produce a **top 20 locations** for this year’s safety budget. Beat a ranking that only counts total incidents. Then change the score (for example add severity or a year-over-year trend) and show how the top 20 moves.

---

## Industrial Significance

- The City already publishes traffic incidents on Open Calgary. Traffic safety teams use this kind of list to argue for signals, lighting, or geometric changes.
- **Who would use this:** City of Calgary Roads / traffic safety. **What is sold:** a defensible shortlist so limited capital hits the worst places first.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load Traffic Incidents. Parse location (community, intersection text, or lat/lon). Drop incomplete rows; say how many.
2. **Reason:** Aggregate to a location key you define (rounded lat/lon, or `INCIDENT INFO` text). Compute count, and at least one extra signal (severity if present, or recent-year share).
3. **Act:** Output top 20 with scores. Baseline = sort by count only.
4. **Iterate:** Change weights; report overlap between the two top-20 lists (how many locations stayed).
5. **Explain:** Three locations that rose or fell and why.

Stretch: join [Traffic Volumes for 2024](https://data.calgary.ca/dataset/Traffic-Volumes-for-2024/cauu-7hnw) to get crashes per volume if the join is feasible.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Aggregate  │ -> │  Rank top 20   │ -> │  Re-weight  │
│ incidents   │    │ by location  │    │ vs count-only  │    │ severity /  │
│ CSV         │    │              │    │                │    │ trend       │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Top 20 by incident count only |
| Your list | Document the extra factor; show Jaccard or overlap vs baseline |
| Transparency | Map or table with location, count, score |
| Loop | ≥ 1 re-weight |
| Honesty | Do not claim you reduced crashes — you ranked locations |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
