# Case 3 — Which wildfires get the next crew?

**Stream:** Software and Computational Math  
**Event:** IEEE YP Industry Hackathon  
**Dates:** October 2–4, 2026 | InceptionU, Calgary

---

## The problem (in plain words)

Alberta does not have infinite crews or air tankers. If you always send the next crew to the **biggest** fire, a smaller fire that is spreading fast in wind can wait. That trade-off was expensive in 2023–2025: the Jasper fire was about **$1.1 billion** in insured losses, and 2025 fires shut in about **7% of Canadian oil** at the peak.

This is a **ranking** problem. You are not simulating fire spread.

**Your challenge:** Rank fires for a limited number of crews. Beat “largest area first.” Then cut crews by **20%** and rebuild the list. Report which fires lost a crew.

You ranked fires. You did **not** put the fire out.

---

## Who would use this

An Alberta Wildfire duty officer. You are selling the **next-crew list** when capacity drops, with a reason you can say out loud.

---

## Steps

1. Load the 2023–2025 fire table. Drop rows missing size or coordinates. Say how many.
2. Score each fire in one line (example: size × wind × dryness, or size + spread rate).
3. Give `N` crews (starter: 40). Baseline = largest size first.
4. Set `N` to 80%. Which fire numbers dropped?
5. Duty-officer paragraph: why these fires, what you skipped.

---

## Picture of the loop

```mermaid
flowchart LR
  A[Load fires] --> B[Score size + weather]
  B --> C[Fill N crews]
  C --> D[20% fewer crews]
  D --> C
```

A **hectare** is 10,000 m² — a bit larger than a soccer pitch.

---

## New words

| Word | Meaning |
|---|---|
| Size class | Alberta’s letter for how big the fire is (A small → E very large) |
| Spread rate | How fast the fire is growing |
| Baseline | Biggest fire first |

---

## Watch or read (optional)

- [Alberta wildfire status](https://www.alberta.ca/wildfire-status)
- [How wildfires grow (simple overview, U.S. National Weather Service)](https://www.weather.gov/safety/wildfire)
- Open data used here: Alberta historical wildfire CSV (see [`data/README.md`](data/README.md))

---

## How we score this case

| What we look for | Target |
|---|---|
| Baseline | Largest size first for the same `N` |
| Your list | Hectares **and** a second signal (wind, dryness, or spread) |
| Loop | One 20% crew cut |

Full rubric: [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).

---

## Start here

1. Open a terminal **in this folder**.
2. `pip install -r requirements.txt`
3. `python agent_starter.py`
4. Change `N` or the score formula and run it again.

Data notes: [`data/README.md`](data/README.md). **Python 3.10+** (3.11 is best).
