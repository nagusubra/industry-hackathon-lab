# Judging Rubric — IEEE YP Industry Hackathon

**Event:** Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | Collision Space, Hunter Hub, University of Calgary  
**Hosted by:** IEEE Southern Alberta Section Young Professionals

Judges score projects using weighted criteria totaling **100%**. Option A (bring your own problem) and Option B (prepared case) use **this same rubric**. Submissions must include a **GitHub repository link** and **project details** (a working demo video link is optional but recommended).

---

## Scoring Summary

| Criteria | Weight |
|---|---|
| Technical Depth | 20% |
| Practical Application / Commercialization in Industry | 15% |
| Autonomous Reasoning & Agent Architecture | 30% |
| Execution, Code Quality & Practicality | 20% |
| Presentation & Demo Quality | 15% |
| **Total** | **100%** |

---

## Criteria & Evaluation Guidance

### 1. Technical Depth — 20%

Does the solution address a real industrial bottleneck with real data and engineering constraints?

**Judges should look for:**

- Clear domain mapping. Not a generic dashboard or productivity wrapper.
- Integration of a real dataset, a named baseline method, and at least one hard constraint (budget, time, physical bound, legal limit).

### 2. Practical Application / Commercialization in Industry — 15%

Would an industry stakeholder actually deploy or commercialize this solution?

**Judges should look for:**

- Clear understanding of the target user, operational workflow, and deployment environment.
- Defined value proposition (who pays, who saves costs, or what safety/operational risk is reduced).
- Realistic scaling pathway from a 48-hour prototype to commercial use.

### 3. Autonomous Reasoning & Agent Architecture — 30%

How well defined is the software architecture? How robust is the agentic loop deployed?

**Judges should look for:**

- A defined loop: data ETL → make a plan → score it → change the plan
- At least one active revision step/epoch based on automated evaluation feedback (e.g., adjusting filters, cutoffs, or routes after scoring).

### 4. Execution, Code Quality & Practicality — 20%

Is the prototype functional, reproducible, and technically sound?

**Judges should look for:**

- Reproducible setup and execution (verifiable seeds, datasets, baselines, and clean GitHub repository instructions).
- Demo is not purely mocked.
- Effective use of tech stack for the problem.

### 5. Presentation & Demo Quality — 15%

Can the team articulate their solution effectively?

**Judges should look for:**

- A crisp problem statement
- Walkthrough of the loop and the baseline comparison

---

## Submission Requirements

Submissions close **Sunday, October 4, 2026 @ 12:00 PM MDT sharp — no exceptions**. Incomplete packages may be ineligible for scoring.

> **Fan Favourite ($100)** is decided separately by community vote (most 👍 reactions on the submission issue), not by this rubric. See [FAN_FAVOURITE.md](FAN_FAVOURITE.md).

### Required Checklist (via the Hackathon Submission issue form — see SUBMISSIONS.md)

- [ ] **Team name + 2–5 members with GitHub handles**, project title, tagline (3 lines max)
- [ ] **GitHub repository link** — public repo containing source code, README, and run instructions
- [ ] **About the project** — inspiration, learnings, build approach, challenges (Markdown + LaTeX)
- [ ] **Screenshots** — min 2, max 5 images proving the app works
- [ ] **Demo video / live-site link** — YouTube/Loom URL (optional but recommended, ≤ 5 minutes)

### Recommended Repository Contents

- Root `README.md` with setup, architecture diagram (text or image), and results
- Reproducible environment (`requirements.txt`, `environment.yml`, or `Dockerfile`)
- Pointers to datasets used (do **not** commit multi-GB raw data; document download steps)
- Evaluation scripts and example outputs / plots

---

## Judging Timeline

| Event | Time (MDT) |
|---|---|
| Submissions Close | Sunday, Oct 4 @ 12:00 PM |
| Judging Window (Active) | Sunday, Oct 4 @ 1:00 PM – 4:00 PM |
| Winners Announced | Sunday, Oct 4 @ 4:00 PM |

---

## Contact

Questions for organizers or sponsorship interest:  
**Subramanian Narayanan**, IEEE SAS YP Chair — [nagusubra@ieee.org](mailto:nagusubra@ieee.org)

*IEEE YP Industry Hackathon | [southern-alberta.ieeecanada.org](https://southern-alberta.ieeecanada.org/)*
