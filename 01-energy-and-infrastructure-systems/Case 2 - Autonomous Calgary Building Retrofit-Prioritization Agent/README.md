# Case 2 — Which Calgary buildings should we retrofit first?

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon  
**Dates:** October 2–4, 2026 | TBA (we will keep you informed), Calgary, AB

---

## The problem (in plain words)

The City owns offices, rec centres, and fire halls. Some use a lot more energy for their size than others. The retrofit budget **cannot** fix every building this year.

This is a spreadsheet job: pick the buildings that save the most energy for the money. Then **re-rank** if the budget or the goal changes (save energy vs cut emissions).

**Your challenge:** Rank buildings under a dollar budget you pick and write down. Beat “fix the biggest building first.” Change the budget or the score once and show which buildings drop off the list.

---

## Who would use this

City Corporate Properties or a contractor. You are selling **more energy saved per public dollar**.

---

## Steps

1. Load the City building file. Drop rows with missing names, area, or energy. Do not invent numbers.
2. Score each building in one sentence (example: energy saved per dollar).
3. The City file has no retrofit cost — **state an assumption** (the starter uses $50 per m²). Fill the budget without going over.
4. Change the budget (for example 80%) or switch “energy first” vs “emissions first.”
5. List who got funded, estimated savings, leftover dollars.

---

## Picture of the loop

```mermaid
flowchart LR
  A[Load buildings] --> B[Score energy per dollar]
  B --> C[Fill the budget]
  C --> D[Smaller budget or new goal]
  D --> C
```

Think of a backpack: you cannot take every item. Take the best value until the bag is full.

---

## New words

| Word | Meaning |
|---|---|
| Retrofit | Upgrade a building so it uses less energy |
| Baseline | Fix the largest building first |
| kWh / GJ | Units of energy (like litres, but for energy) |

---

## Watch or read (optional)

- [ENERGY STAR for buildings (Natural Resources Canada)](https://natural-resources.canada.ca/energy-efficiency/energy-star)
- [Open Calgary — City building energy](https://data.calgary.ca/) (search “building energy” or use the file in `data/`)

---

## How we score this case

| What we look for | Target |
|---|---|
| Baseline | Biggest-first under the same budget |
| Your list | More energy saved per dollar, or same savings for less spend |
| Loop | Re-rank after one budget or weight change |
| Honesty | Do not spend more than `B`; no duplicate buildings |

Full rubric: [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).

---

## Start here

1. Open a terminal **in this folder**.
2. `pip install -r requirements.txt`
3. `python agent_starter.py`
4. Change the budget or the score and run it again.

Data notes: [`data/README.md`](data/README.md). **Python 3.10+** (3.11 is best).
