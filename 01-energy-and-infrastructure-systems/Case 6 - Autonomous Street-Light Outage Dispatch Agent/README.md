# Case 6 — Autonomous Street-Light Outage Dispatch Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

When a street light is out, Calgarians call **311**. Crews cannot visit every pole the same day. If dispatch is “oldest ticket first,” a dark corridor by a school can wait behind a single lamp on a quiet street.

**Your challenge:** From 311 requests about street lights (and similar electrical tickets), build a **this-week dispatch list**. Beat “oldest ticket first.” Then pretend one crew calls in sick (drop 20% capacity) and **rebuild the list**.

---

## Industrial Significance

- 311 is how The City hears about failed electrical assets in the public realm. Repeat outages in the same community are a signal, not noise.
- **Who would use this:** City of Calgary Roads / Street Lighting. **What is sold:** fewer dark nights per crew-hour.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load 311 service requests. Filter to street lighting / electrical (inspect `service_name` or equivalent). Keep community, open date, status.
2. **Reason:** Score tickets (age, repeats in the same community, open vs closed). State the formula.
3. **Act:** Assume `N` crew-slots for the week (you pick `N`, e.g. 40). Output the chosen tickets. Baseline = oldest `N` tickets.
4. **Iterate:** Set `N` to `0.8 * N` and re-select; report which communities lost coverage.
5. **Explain:** A dispatcher paragraph: why these tickets, what you skipped.

Stretch: predict next week’s volume by community (simple counts by month) vs last month’s count.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Score      │ -> │  Fill N slots  │ -> │  Cut N      │
│ 311 lights  │    │ age + repeats│    │ vs oldest-first│    │ 20% and     │
│ tickets     │    │              │    │                │    │ re-pick     │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md).

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Oldest-first (`FIFO`) for the same `N` |
| Your list | Show average ticket age **and** repeat-community coverage vs FIFO |
| Loop | ≥ 1 capacity shock (sick crew) |
| Filter | Document how you identified lighting tickets |
| Demo | Table: community, ticket id, score, selected yes/no |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
