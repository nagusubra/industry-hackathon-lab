# Case 1 — Autonomous Alberta Peak-Price Load-Shift Agent

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

In Alberta, the wholesale electricity price (the **pool price**) can be a few dollars one hour and hundreds of dollars the next. A Calgary factory, a downtown office, or a City recreation centre that runs the same way every hour is leaving money on the table — and often burning extra gas when the grid is tight.

You do not need to model the whole power system. You need a **simple rule that can change**: look at past prices and load, mark the expensive hours, and say when to run machines, charge a battery, or wait.

**Your challenge:** Build a small decision loop that reads AESO hourly prices (and load), recommends when to use electricity vs wait, scores the bill against a naive “always on” plan, then **changes the rule once** and shows whether the bill got better.

---

## Industrial Significance

- Hackathon is in Calgary. AESO is the operator of Alberta’s wholesale market. Local plants, data centres, and City facilities all pay into this price.
- Storage pilots and flexible industrial load are growing; a 48-hour tool that flags expensive hours is something a facilities manager can understand on Monday.
- **Who would use this:** a City of Calgary energy manager, an industrial load customer, or a retailer hedging pool-price risk. **What is sold:** fewer dollars spent on the same kWh by shifting *when* work happens.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load a CSV of hourly Alberta pool price and Alberta Internal Load (AIL). Use a held-out week or month you do not tune on.
2. **Reason:** Define “expensive” in a way you can explain (for example top 10% of hours, or price above a dollar threshold).
3. **Act:** Output a schedule: charge / run / idle for each hour. Keep it physically simple (you cannot charge and discharge at the same time; optional battery with a size you pick).
4. **Iterate:** After you score the first schedule, change one thing (threshold, battery size, or “never run 5–8 p.m.”) and score again.
5. **Explain:** A short operator note: dollars saved vs always-on, hours shifted, and when the rule fails (for example an unexpected price spike).

Stretch: add wind or gas share from the same AESO files; compare to a second naive rule (“never run after 5 p.m.”).

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Score bill    │ -> │  Revise     │
│ AESO price  │    │ expensive    │    │ vs always-on   │    │ threshold   │
│ + AIL hours │    │ hour flags   │    │                │    │ or window   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py) (`pip install -r requirements.txt`). See [`data/README.md`](data/README.md) for the bundled 2024 AESO CSV.

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Cost vs always-on | Report $ (or $ / MWh) on held-out hours; show a table |
| Second baseline | Also beat or report vs a fixed clock rule (e.g. never run 17:00–20:00) |
| Feasibility | No impossible battery actions if you model storage |
| Loop | ≥ 1 revise after seeing the first score |
| Demo | Runnable in the 48-hour window |

Judges will prioritize **a clear dollar story + one honest revision** over a complex model. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
