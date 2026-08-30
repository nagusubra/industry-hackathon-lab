# Case 4 — How many more trips can this engine make?

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon  
**Dates:** October 2–4, 2026 | InceptionU, Calgary

---

## The problem (in plain words)

A bus or a truck should not die on 17th Avenue. The real question is: **how many more trips before we pull it in?**

Calgary Transit does not publish engine-sensor spreadsheets. NASA published a public jet-engine wear set that is the **same job**: readings over time → remaining life → inspect now vs later. You practice on that file and tell the story as a **fleet shop** tool.

**Your challenge:** Guess remaining life (how many cycles are left). Draw an “inspect this week” line. Count missed failures vs extra inspections. **Move the line once** and show the new trade-off.

This case is **harder** than the others (it uses a small linear model). Ask a mentor if you have not seen a line of best fit.

---

## Who would use this

Calgary Transit / Fleet (the method), or a private shop. You are selling **fewer roadside failures** without checking every vehicle every night.

---

## Steps

1. Load NASA C-MAPSS **FD001 only** (one condition, one fault type).
2. Remaining life on training engines = last cycle minus current cycle.
3. Fit a simple model (the starter uses a straight line on a few sensors). No deep learning.
4. On the test engines, flag “inspect now” if predicted life is below a number you pick.
5. Change that number; report missed failures vs extra inspections.

---

## Picture of the loop

```mermaid
flowchart LR
  A[Load engine sensors] --> B[Guess remaining cycles]
  B --> C[Inspect if guess is low]
  C --> D[Move the inspect line]
  D --> C
```

If you inspect too early, you waste shop time. If you inspect too late, the engine fails on the road.

---

## New words

| Word | Meaning |
|---|---|
| Remaining useful life (RUL) | How many cycles until failure |
| MAE | Mean absolute error — average how far off your guess is |
| Threshold | The cutoff that means “bring it in this week” |

---

## Watch or read (optional)

- [Predictive maintenance (Wikipedia)](https://en.wikipedia.org/wiki/Predictive_maintenance)
- [Linear regression, clearly explained (StatQuest on YouTube)](https://www.youtube.com/watch?v=7ArmBVF2dCs)
- NASA C-MAPSS is the bundled `train_FD001.txt` / `test_FD001.txt` in `data/` — do **not** download FD002–FD004 on hour one.

---

## How we score this case

| What we look for | Target |
|---|---|
| RUL error | MAE or RMSE vs NASA’s `RUL_FD001.txt` |
| Baseline | A single-sensor guess, plus your model |
| Loop | Move the inspect line at least once |
| Scope | FD001 only |

Full rubric: [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).

---

## Start here

1. Open a terminal **in this folder**.
2. `pip install -r requirements.txt`
3. `python agent_starter.py`
4. Change the inspect cutoff (30 vs 50 cycles) and run it again.

Data notes: [`data/README.md`](data/README.md). **Python 3.10+** (3.11 is best).
