# Case 6 — Which street lights should we fix this week?

**Stream:** Energy and Infrastructure Systems  
**Event:** IEEE YP Industry Hackathon  
**Dates:** October 2–4, 2026 | InceptionU, Calgary

---

## The problem (in plain words)

When a street light is out, people call **311**. Crews cannot visit every pole the same day. If you always take the **oldest** ticket, a dark stretch by a school can wait behind one lamp on a quiet street.

**Your challenge:** Build a **this-week list**. Beat oldest-first. Then pretend one crew is sick (20% fewer visits) and **rebuild the list**.

---

## Who would use this

City of Calgary Roads / Street Lighting. You are selling **fewer dark nights per crew-hour**.

---

## Steps

1. Load 311 lighting tickets. Keep community and date.
2. Score each ticket (age, and how many times that community called). Write the formula in one line.
3. Fill `N` slots (the starter uses 40). Baseline = oldest `N`.
4. Set `N` to 80% and pick again. Which communities lost a visit?
5. Write a dispatcher paragraph: why these tickets, what you skipped.

---

## Picture of the loop

```mermaid
flowchart LR
  A[Load 311 light tickets] --> B[Score age + repeats]
  B --> C[Fill N crew slots]
  C --> D[20% fewer crews]
  D --> C
```

**FIFO** = first in, first out = oldest ticket first. That is the plan you must beat.

---

## New words

| Word | Meaning |
|---|---|
| FIFO | Oldest request first |
| Dispatch | Choosing which jobs the crew does today |
| Repeat | The same community calling again |

---

## Watch or read (optional)

- [Calgary 311](https://www.calgary.ca/311.html)
- [Queues: first in, first out (Wikipedia)](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics))

---

## How we score this case

| What we look for | Target |
|---|---|
| Baseline | Oldest-first for the same `N` |
| Your list | Age **and** repeat-community coverage vs FIFO |
| Loop | One sick-crew cut |

Full rubric: [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).

---

## Start here

1. Open a terminal **in this folder**.
2. `pip install -r requirements.txt`
3. `python agent_starter.py`
4. Change `N` or the score and run it again.

Data notes: [`data/README.md`](data/README.md). **Python 3.10+** (3.11 is best).
