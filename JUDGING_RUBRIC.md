# Judging Rubric — IEEE YP Industry Hackathon

**Event:** Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta  
**Hosted by:** IEEE Southern Alberta Section Young Professionals

Judges score projects out of **100 total points**. Option A (bring your own problem) and Option B (prepared case) use **this same rubric**. Submissions must include a **GitHub repository link**, **project details**, and a **working demo video link**.

---

## Scoring Summary

| Criteria | Weight | Points |
|---|---|---|
| Technical Depth | 20% | 20 |
| Practical Application / Commercialization in Industry | 15% | 15 |
| Autonomous Reasoning & Agent Architecture | 30% | 30 |
| Execution, Code Quality & Practicality | 20% | 20 |
| Presentation & Demo Quality | 15% | 15 |
| **Total** | **100%** | **100** |

---

## Criteria & Evaluation Guidance

### 1. Technical Depth — 20%

Does the solution address a real industrial bottleneck with real data, constraints, and numbers — not a chatbot wrapper? A high-school team can score well here with a clear spreadsheet loop.

**Judges should look for:**

- A clear mapping to energy, infrastructure, operations, materials, or chemistry (not a generic productivity app)
- Use of a real dataset, a named baseline, and at least one engineering constraint (budget, time, a legal limit, a physical bound)
- Evidence that the output would matter to a practitioner (a ranked list, a schedule, a flag, a mix — not only a dashboard)

### 2. Practical Application / Commercialization in Industry — 15%

Would someone in Calgary, Alberta, or Canadian industry actually use this?

**Judges should look for:**

- A named user (City business unit, AESO, a retailer, a plant, a contractor)
- A sentence on who pays, who saves, or who is safer if the tool works
- Honest scope: a 48-hour prototype that could grow into a product or internal tool

### 3. Autonomous Reasoning & Agent Architecture — 30%

How robust is the loop? A single LLM answer with no evaluation does not score well here.

**Judges should look for:**

- A defined loop: read data → make a plan → score it → change the plan
- At least one revise step (change a cutoff, a filter, a route, or a ranking after seeing a score)
- Tooling against CSVs, a simple simulator, or a solver — not slides alone

### 4. Execution, Code Quality & Practicality — 20%

Is the prototype runnable in the 48-hour window?

**Judges should look for:**

- Clear install/run instructions and a coherent repo
- Reproducible numbers (seed, date range, baseline)
- Evidence the demo is not purely mocked

### 5. Presentation & Demo Quality — 15%

Can the team explain their own numbers?

**Judges should look for:**

- A crisp problem statement a non-specialist can follow
- Walkthrough of the loop and the baseline comparison
- A time-boxed demo video and honest limitations

---

## Submission Requirements

Submissions close **Sunday, October 4, 2026 @ 12:00 PM MST**. Incomplete packages may be ineligible for scoring.

### Required Checklist

- [ ] **GitHub repository link** — public or judge-accessible repo containing source code, README, and run instructions
- [ ] **Project details** — problem statement, architecture overview, datasets used, quantitative results / metrics
- [ ] **Working demo video link** — screen recording or presentation walkthrough (recommended ≤ 5 minutes)

### Recommended Repository Contents

- Root `README.md` with setup, architecture diagram (text or image), and results
- Reproducible environment (`requirements.txt`, `environment.yml`, or `Dockerfile`)
- Pointers to datasets used (do **not** commit multi-GB raw data; document download steps)
- Evaluation scripts and example outputs / plots

---

## Judging Timeline

| Event | Time (MST) |
|---|---|
| Submissions Close | Sunday, Oct 4 @ 12:00 PM |
| Judging Window (Active) | Sunday, Oct 4 @ 1:00 PM – 4:00 PM |
| Winners Announced | Sunday, Oct 4 @ 4:00 PM |

---

## Contact

Questions for organizers or sponsorship interest:  
**Subramanian Narayanan**, IEEE SAS YP Chair — [nagusubra@ieee.org](mailto:nagusubra@ieee.org)

*IEEE YP Industry Hackathon | [southern-alberta.ieeecanada.org](https://southern-alberta.ieeecanada.org/)*
