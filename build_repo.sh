#!/usr/bin/env bash
# =============================================================================
# IEEE YP Industry Hackathon Lab — Repository Builder
# Event: IEEE YP Industry Hackathon: Autonomous Intelligence for Industrial Innovation
# Dates: October 2–4, 2026 | Location: InceptionU, Calgary, Alberta
# Hosted by: IEEE Southern Alberta Section Young Professionals
# =============================================================================
# Usage: bash build_repo.sh
# Generates the full industry-hackathon-lab directory tree and documentation.
#
# NOTE: After the first generation, the committed files in this repository are
# the source of truth. Re-running this script will overwrite local edits.
# Prefer editing the generated Markdown/Python files directly for content fixes.
# =============================================================================

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "==> Building IEEE YP Industry Hackathon Lab repository in: $ROOT"

# ---------------------------------------------------------------------------
# Directory tree
# ---------------------------------------------------------------------------
mkdir -p "01-energy-systems-environmental-modeling/Case 1 - Autonomous Grid-Balancing Agent for Renewable Wind Integration/data"
mkdir -p "02-applied-physics-aerospace-electrical/Case 1 - Autonomous Structural-Health and Aerodynamic-Design Agent/data"
mkdir -p "03-software-cryptography-computational-math/Case 1 - Autonomous Quantum-Safe Cryptography Migration Agent/data"
mkdir -p "04-materials-science-chemical-synthesis/Case 1 - Autonomous Battery Cathode Discovery Agent/data"
mkdir -p "05-life-sciences-bio-engineering/Case 1 - Autonomous Protein-Structure-to-Toxicity Screening Agent/data"

# ---------------------------------------------------------------------------
# Root README.md
# ---------------------------------------------------------------------------
cat << 'EOF' > "$ROOT/README.md"
# IEEE YP Industry Hackathon: Autonomous Intelligence for Industrial Innovation

[![Repo traffic](https://raw.githubusercontent.com/nagusubra/traffic/main/doc/metric/industry-hackathon-lab/badge.svg)](https://nagusubra.github.io/traffic/doc/metric/industry-hackathon-lab/)

**Hosted by:** IEEE Southern Alberta Section Young Professionals (IEEE SAS YP)  
**Dates:** Friday, October 2 – Sunday, October 4, 2026  
**Duration:** 48-hour hackathon  
**Location:** InceptionU, Calgary, Alberta  
**Website:** [southern-alberta.ieeecanada.org](https://southern-alberta.ieeecanada.org/)

---

## Partners

| Partner | Role | Link |
|---|---|---|
| **IEEE** | Host / Organizer | [southern-alberta.ieeecanada.org](https://southern-alberta.ieeecanada.org/) |
| **TechConnect Alberta** | Ecosystem partner | [techconnect.amgfoundation.ca](https://techconnect.amgfoundation.ca/) |
| **Eudaimonia** | Community volunteers | [luma.com/eudaimonia](https://luma.com/eudaimonia) |
| **Young Energy Infrastructure Professionals** | Community partner | [yeip.energy](https://yeip.energy/) |
| **Cursor** | AI coding partner | [cursor.com/home](https://cursor.com/home) |

---

## Mission

Unlike typical hackathons that yield surface-level chat interfaces or basic productivity apps, our mission is to deliver **hard-science technical value**. Collaborative teams of 2 to 5 young professionals and recent graduates will spend 48 hours building **Autonomous AI Agents** (or agent frameworks) designed to solve complex scientific and engineering bottlenecks across modern industrial sectors — moving beyond chat wrappers into deep physical infrastructure, computational science, and industrial systems.

---

## Event Schedule (MST)

| Phase / Event | Date & Time (MST) | Notes |
|---|---|---|
| Official Kickoff | Friday, Oct 2 @ 5:00 PM | Opening remarks, track briefing, team formation |
| Submissions Close | Sunday, Oct 4 @ 12:00 PM | Teams submit projects, GitHub links & video demos |
| Judging Window (Active) | Sunday, Oct 4 @ 1:00 PM – 4:00 PM | Mandatory scoring & deliberation |
| Winners Announced | Sunday, Oct 4 @ 4:00 PM | Judges present awards |
| Hackathon Wrap-up | Sunday, Oct 4 @ 5:00 PM | Closing remarks and networking |

---

## Eligibility & Teams

- **Eligibility:** Open to all — students, professionals, IEEE members, and non-members. We welcome local innovators, recent graduates, and brilliant young professionals.
- **Team size:** Collaborative teams of **2 to 5 members**.
- **Format:** In-person, 48-hour build sprint at InceptionU.

---

## Prizes

| Place | Prize (CAD) |
|---|---|
| 1st Place | $200 |
| 2nd Place | $150 |
| 3rd Place | $100 |

---

## Judges & Sponsors

Judges & Sponsors: **to be announced**.

If you have any suggestions or would like to become a sponsor for the hackathon, please contact the Chair (below).

---

## Registration & Contact

- **Registration:** `[REGISTRATION LINK - TBD]`
- **Contact / Sponsorship:** Subramanian Narayanan, IEEE SAS YP Chair — [nagusubra@ieee.org](mailto:nagusubra@ieee.org)

---

## Judging

Projects are scored out of **100 points**. See [JUDGING_RUBRIC.md](JUDGING_RUBRIC.md) for full criteria and submission requirements.

**Required submission package (by Sunday, Oct 4 @ 12:00 PM MST):**
1. GitHub repository link
2. Project details / documentation
3. Working demo video link

---

## Industrial Tracks (Table of Contents)

Each stream has **four** case studies. Teams pick **one** case.

### 1. Energy Systems & Environmental Modeling

Agents for autonomous power grid load-balancing, optimizing renewable energy storage cycles, or running complex environmental simulations to predict the impact of carbon sequestration technologies.

| Case | Title |
|---|---|
| 1 | [Autonomous Grid-Balancing Agent for Renewable Wind Integration](01-energy-systems-environmental-modeling/Case%201%20-%20Autonomous%20Grid-Balancing%20Agent%20for%20Renewable%20Wind%20Integration/README.md) |
| 2 | [Autonomous Storage-Dispatch Agent for Building PV and Battery](01-energy-systems-environmental-modeling/Case%202%20-%20Autonomous%20Storage-Dispatch%20Agent%20for%20Building%20PV%20and%20Battery/README.md) |
| 3 | [Autonomous Second-Life Battery Degradation-Economics Agent](01-energy-systems-environmental-modeling/Case%203%20-%20Autonomous%20Second-Life%20Battery%20Degradation-Economics%20Agent/README.md) |
| 4 | [Autonomous Alberta Grid Real-Time Balancing Agent](01-energy-systems-environmental-modeling/Case%204%20-%20Autonomous%20Alberta%20Grid%20Real-Time%20Balancing%20Agent/README.md) |

### 2. Applied Physics, Aerospace & Electrical Engineering

Agents that autonomously iteratively refine CAD designs for wind resistance, conduct real-time structural health monitoring for infrastructure, or optimize flight path dynamics for fuel efficiency in aerospace.

| Case | Title |
|---|---|
| 1 | [Autonomous Structural-Health and Aerodynamic-Design Agent](02-applied-physics-aerospace-electrical/Case%201%20-%20Autonomous%20Structural-Health%20and%20Aerodynamic-Design%20Agent/README.md) |
| 2 | [Autonomous Bridge Structural-Health Monitoring Agent](02-applied-physics-aerospace-electrical/Case%202%20-%20Autonomous%20Bridge%20Structural-Health%20Monitoring%20Agent/README.md) |
| 3 | [Autonomous Electromechanical Drive Fault-Diagnosis Agent](02-applied-physics-aerospace-electrical/Case%203%20-%20Autonomous%20Electromechanical%20Drive%20Fault-Diagnosis%20Agent/README.md) |
| 4 | [Autonomous Battery Health and RUL Agent](02-applied-physics-aerospace-electrical/Case%204%20-%20Autonomous%20Battery%20Health%20and%20RUL%20Agent/README.md) |

### 3. Software, Cryptography & Computational Math

Agents that automate the transition to quantum-safe encryption protocols, optimize low-level compiler performance for specialized hardware, or solve high-dimensional optimization problems in industrial logistics and robotics.

| Case | Title |
|---|---|
| 1 | [Autonomous Quantum-Safe Cryptography Migration Agent](03-software-cryptography-computational-math/Case%201%20-%20Autonomous%20Quantum-Safe%20Cryptography%20Migration%20Agent/README.md) |
| 2 | [Autonomous Compiler-Config Search Agent](03-software-cryptography-computational-math/Case%202%20-%20Autonomous%20Compiler-Config%20Search%20Agent/README.md) |
| 3 | [Autonomous Disruption-Aware Job-Shop Scheduling Agent](03-software-cryptography-computational-math/Case%203%20-%20Autonomous%20Disruption-Aware%20Job-Shop%20Scheduling%20Agent/README.md) |
| 4 | [Autonomous Combinatorial Optimization Search Agent](03-software-cryptography-computational-math/Case%204%20-%20Autonomous%20Combinatorial%20Optimization%20Search%20Agent/README.md) |

### 4. Materials Science & Chemical Synthesis

Agents that autonomously search for new battery cathode materials, optimize catalyst performance in chemical reactors, or design sustainable polymers with specific heat-resistance properties.

| Case | Title |
|---|---|
| 1 | [Autonomous Battery Cathode Discovery Agent](04-materials-science-chemical-synthesis/Case%201%20-%20Autonomous%20Battery%20Cathode%20Discovery%20Agent/README.md) |
| 2 | [Autonomous Reaction-Condition Optimizer](04-materials-science-chemical-synthesis/Case%202%20-%20Autonomous%20Reaction-Condition%20Optimizer/README.md) |
| 3 | [Autonomous Catalyst Discovery Agent](04-materials-science-chemical-synthesis/Case%203%20-%20Autonomous%20Catalyst%20Discovery%20Agent/README.md) |
| 4 | [Autonomous Sustainable Polymer Design Agent](04-materials-science-chemical-synthesis/Case%204%20-%20Autonomous%20Sustainable%20Polymer%20Design%20Agent/README.md) |

### 5. Life Sciences & Bio-Engineering

Agents for autonomous protein folding analysis, automating wet-lab to dry-lab data loops, or predicting toxicological profiles of new compounds.

| Case | Title |
|---|---|
| 1 | [Autonomous Protein-Structure-to-Toxicity Screening Agent](05-life-sciences-bio-engineering/Case%201%20-%20Autonomous%20Protein-Structure-to-Toxicity%20Screening%20Agent/README.md) |
| 2 | [Autonomous Enzyme Stability Engineering Agent](05-life-sciences-bio-engineering/Case%202%20-%20Autonomous%20Enzyme%20Stability%20Engineering%20Agent/README.md) |
| 3 | [Autonomous Multi-Endpoint ADMET Risk Triage Agent](05-life-sciences-bio-engineering/Case%203%20-%20Autonomous%20Multi-Endpoint%20ADMET%20Risk%20Triage%20Agent/README.md) |
| 4 | [Autonomous Binding-Affinity Discovery Agent](05-life-sciences-bio-engineering/Case%204%20-%20Autonomous%20Binding-Affinity%20Discovery%20Agent/README.md) |

---

## Repository Layout

```
industry-hackathon-lab/
├── README.md
├── LICENSE
├── JUDGING_RUBRIC.md
├── build_repo.sh
├── 01-energy-systems-environmental-modeling/
├── 02-applied-physics-aerospace-electrical/
├── 03-software-cryptography-computational-math/
├── 04-materials-science-chemical-synthesis/
└── 05-life-sciences-bio-engineering/
```

Each case folder includes a problem brief (`README.md`), dataset guide (`data/README.md`), Python dependency list (`requirements.txt`), and a starter agent skeleton (`agent_starter.py`).

---

## Getting Started

**Requires Python 3.10+ (3.11 recommended).**

1. Register via the registration link above (when published).
2. Form a team of 2–5 members and pick **one** industrial stream/case.
3. Clone this lab repository and follow the case `README.md` + `data/README.md`.
4. Create a venv, install the case `requirements.txt`, and extend `agent_starter.py`.
5. Build an autonomous agent that reasons, tools, and acts on real industrial data.
6. Submit your GitHub repo, project write-up, and demo video by **Sunday, Oct 4 @ 12:00 PM MST**.

---

## License

This laboratory repository is released under the [MIT License](LICENSE).  
© 2026 IEEE Southern Alberta Section Young Professionals

---

*IEEE YP Industry Hackathon | [southern-alberta.ieeecanada.org](https://southern-alberta.ieeecanada.org/)*
EOF

# ---------------------------------------------------------------------------
# JUDGING_RUBRIC.md
# ---------------------------------------------------------------------------
cat << 'EOF' > "$ROOT/JUDGING_RUBRIC.md"
# Judging Rubric — IEEE YP Industry Hackathon

**Event:** Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta  
**Hosted by:** IEEE Southern Alberta Section Young Professionals

To ensure a fair and practical evaluation, judges will score projects out of **100 total points** based on four core criteria. Submissions must include a **GitHub repository link**, **project details**, and a **working demo video link**.

---

## Scoring Summary

| Criteria | Weight | Points |
|---|---|---|
| Technical Depth & "Hard Science" Value | 35% | 35 |
| Autonomous Reasoning & Agent Architecture | 30% | 30 |
| Execution, Code Quality & Practicality | 20% | 20 |
| Presentation & Demo Quality | 15% | 15 |
| **Total** | **100%** | **100** |

---

## Criteria & Evaluation Guidance

### 1. Technical Depth & "Hard Science" Value — 35%

Does the solution address a genuine, complex industrial bottleneck? Projects must move beyond trivial productivity gains or surface-level chat wrappers to deliver deep engineering or mathematical value.

**Judges should look for:**
- Clear mapping to a physical, chemical, cryptographic, aerospace, or life-science bottleneck (not a generic chatbot wrapper)
- Use of domain equations, simulations, scientific datasets, or engineering constraints
- Evidence that the agent output would matter to an industrial practitioner

### 2. Autonomous Reasoning & Agent Architecture — 30%

How robust is the AI agent or framework? Evaluate its capacity for autonomous reasoning, iterative execution loops, interaction with external tools/simulations, and handling complex industrial data.

**Judges should look for:**
- A defined agent loop (perceive → reason → act / tool-use → evaluate)
- Iterative refinement rather than a single one-shot LLM call
- Tooling against simulations, APIs, solvers, compilers, or scientific databases
- Handling of noisy, multi-modal, or high-dimensional industrial data

### 3. Execution, Code Quality & Practicality — 20%

Is the framework functional and technically sound? Assess the operational viability of the prototype created during the 48-hour window, as evidenced by their GitHub repository code quality and architectural structure.

**Judges should look for:**
- Runnable prototype with clear install/run instructions
- Coherent repository structure, readable code, and reproducible experiments
- Sensible engineering trade-offs given the 48-hour constraint
- Evidence the demo is not purely mocked / slideware

### 4. Presentation & Demo Quality — 15%

How effectively did the team articulate their problem statement and engineering value? The video demo and project details should provide a clear, concise, and professional explanation of the solution.

**Judges should look for:**
- Crisp problem statement and industrial significance
- Clear walkthrough of agent architecture and results
- Professional, time-boxed demo video
- Honest discussion of limitations and next steps

---

## Submission Requirements

Submissions close **Sunday, October 4, 2026 @ 12:00 PM MST**. Incomplete packages may be ineligible for scoring.

### Required Checklist

- [ ] **GitHub repository link** — public or judge-accessible repo containing source code, README, and run instructions
- [ ] **Project details** — problem statement, architecture overview, datasets used, quantitative results / metrics
- [ ] **Working demo video link** — screen recording or presentation walkthrough of the agent in action (recommended ≤ 5 minutes)

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
EOF

# ---------------------------------------------------------------------------
# LICENSE (MIT)
# ---------------------------------------------------------------------------
cat << 'EOF' > "$ROOT/LICENSE"
MIT License

Copyright (c) 2026 IEEE Southern Alberta Section Young Professionals

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# =============================================================================
# STREAM 1 — Energy Systems & Environmental Modeling
# =============================================================================
CASE1="01-energy-systems-environmental-modeling/Case 1 - Autonomous Grid-Balancing Agent for Renewable Wind Integration"

cat << 'EOF' > "$ROOT/$CASE1/README.md"
# Case 1 — Autonomous Grid-Balancing Agent for Renewable Wind Integration

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Modern power grids must continuously balance supply and demand while absorbing highly variable wind generation. Forecast errors, ramp events, and transmission constraints create real operational risk: curtailment of renewables, expensive peaker plant dispatch, and — in extreme cases — frequency instability.

**Your challenge:** Build an **autonomous AI agent** that ingests wind resource / power forecasts and load time series, reasons about grid imbalance risk, and iteratively proposes (and evaluates) dispatch / storage / curtailment actions against a physics-aware power system model — not a chat wrapper over a static dashboard.

---

## Industrial Significance

- Wind variability is a first-order bottleneck for high-renewable grids in Alberta and across North America.
- Grid operators (ISOs / utilities) already consume NREL-class meteorological and forecast products; agents that close the loop from forecast → action are industrially relevant.
- Alberta’s electricity system and Canadian net-zero pathways depend on reliable renewable integration with storage and flexible loads.
- Solutions that reduce imbalance penalties, curtailment, or reserve requirements have direct economic and environmental value.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest open wind and load datasets (NREL WIND Toolkit subsets and/or NREL PERFORM Phase II ISO forecasts; optional PJM hourly load for demand-side experiments).
2. **Predict:** Produce short-horizon wind power and net-load forecasts with uncertainty estimates.
3. **Optimize:** Formulate a dispatch / storage schedule (e.g., via PyPSA linear optimal power flow or a simplified balancing-area model) that respects capacity and energy constraints.
4. **Act & Iterate:** Implement an agent loop that proposes actions, evaluates them in simulation, and revises plans when forecast error or constraint violations appear.
5. **Explain:** Emit operator-facing summaries: imbalance risk, recommended reserve, curtailment vs. storage trade-offs.

Stretch goals: couple OpenFAST / turbine physics for site-specific power curves; multi-zone balancing with transmission limits; carbon intensity of the resulting dispatch.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ wind+load   │    │ forecast +   │    │ PyPSA / reV /  │    │ dispatch &  │
│ time series │    │ risk policy  │    │ OpenFAST tools │    │ metrics     │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter frameworks (open source):**
- [PyPSA](https://github.com/PyPSA/pypsa) — Python for Power System Analysis (network + LOPF optimization)
- [OpenFAST](https://github.com/OpenFAST/openfast) — NREL whole-turbine aero-hydro-servo-elastic simulation
- NREL [WIND Toolkit on AWS](https://registry.opendata.aws/nrel-pds-wtk/) — meteorological + power estimates
- [PERFORM Forecasts documentation](https://github.com/PERFORM-Forecasts/documentation) — ISO load/wind/solar actuals + probabilistic forecasts
- Optional: NREL `reV` for renewable potential modeling

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — perceive / reason / act skeleton wired to a local CSV path
- [`requirements.txt`](requirements.txt) — core Python dependencies
- [`data/README.md`](data/README.md) — verified dataset links, schemas, and download commands

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Net-load forecast MAE or RMSE | Report vs. naive persistence baseline |
| Imbalance energy (MWh) | Reduce vs. no-control / greedy baseline over a held-out week |
| Curtailment fraction | Minimize while meeting demand + reserve constraints |
| Storage SOC feasibility | Zero hard constraint violations in the simulated horizon |
| Agent loop autonomy | ≥ 1 closed-loop iteration (propose → simulate → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **hard-science grid physics + autonomous tool use** over UI polish alone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
EOF

cat << 'EOF' > "$ROOT/$CASE1/data/README.md"
# Data Guide — Grid-Balancing Agent (Stream 1)

This case uses **real, open-access** energy datasets. Do **not** commit multi-GB raw archives to GitHub; download locally into this folder (or a sibling `raw/` directory) and document your subset.

---

## Primary Datasets

### 1. NREL Wind Integration National Dataset (WIND) Toolkit

- **What:** Meteorological fields + estimated turbine power for 100,000+ CONUS sites (2007–2013 era toolkit; long-term ensemble / LED extensions available).
- **Host:** AWS Open Data — `s3://nrel-pds-wtk/`
- **Docs:** https://registry.opendata.aws/nrel-pds-wtk/  
  Overview: https://nlr.gov/grid/wind-toolkit
- **Formats:** HDF5 / NetCDF-style scientific arrays on S3; derived CSV/parquet subsets commonly used in ML pipelines
- **License:** DOE Open Energy Data Initiative (public)

**List bucket (no AWS account required):**

```bash
aws s3 ls --no-sign-request s3://nrel-pds-wtk/
```

**Example: download a small site subset (adjust keys after listing):**

```bash
mkdir -p raw/wtk
aws s3 cp --no-sign-request s3://nrel-pds-wtk/ raw/wtk/ --recursive --exclude "*" --include "*README*"
# Then select a specific site/year HDF5 path from the listing for your agent pipeline.
```

**Typical fields (site power / met subsets):** timestamp, wind speed / direction at hub height (e.g., 100 m), temperature, pressure, estimated power (MW), forecast horizons (1 h / 4 h / 6 h / 24 h where forecast products are available).

### 2. NREL PERFORM Phase II — Solar, Wind, and Load Forecasts (MISO, NYISO, SPP)

- **What:** Time-coincident load, wind, and solar **actuals** and **probabilistic forecasts** for three U.S. ISOs (actuals ~2018–2019; forecasts primarily 2019).
- **Docs / access:** https://github.com/PERFORM-Forecasts/documentation  
  Technical report: https://doi.org/10.2172/2335360
- **Formats:** CSV / structured time-series packages documented in the PERFORM repo
- **Spatial scales:** site-level, zone-level, system (balancing area) level
- **Why useful:** Perfect for agent experiments that couple renewable forecasts with system load.

```bash
git clone https://github.com/PERFORM-Forecasts/documentation.git raw/perform-docs
# Follow the documentation README for dataset download URLs and directory layout.
```

### 3. Kaggle — Hourly Energy Consumption (PJM / related ISO load series)

- **What:** Convenient hourly load CSVs for rapid prototyping of demand-side imbalance models.
- **URL:** https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption
- **Format:** CSV (`Datetime`, regional load MW columns)
- **Use:** Pair with a wind power series (WTK or PERFORM) as a lightweight balancing sandbox if full ISO PERFORM packages are too large for day-one setup.

```bash
# Requires Kaggle API credentials (~/.kaggle/kaggle.json)
kaggle datasets download -d robikscube/hourly-energy-consumption -p raw/pjm --unzip
```

### 4. Optional Kaggle — Feature-Engineered Wind Time Series (WTK-LED derived)

- **URL:** https://www.kaggle.com/datasets/muratiik/feature-engineered-wind-time-series-data-2015-23
- **Format:** CSV (~hourly, engineered shear/veer/regime labels + estimated power)
- **License:** CC BY 4.0
- **Use:** Fast ML baseline when you cannot stage multi-TB WTK HDF5 locally during the hackathon.

---

## Suggested Local Layout

```
data/
├── README.md          # this file
└── raw/               # gitignored downloads
    ├── wtk/
    ├── perform/
    └── pjm/
```

Add a `.gitignore` entry for `raw/` in your team repo.

---

## Loading Example (Python)

```python
import pandas as pd

# After placing a CSV subset next to this folder:
df = pd.read_csv("raw/pjm/AEP_hourly.csv", parse_dates=["Datetime"])
df = df.sort_values("Datetime").set_index("Datetime")
print(df.head())
```

For WTK HDF5 site files, use `h5py` / `xarray` after downloading a specific object from `s3://nrel-pds-wtk/`.

---

## Citation Notes

When you publish results, cite NREL WIND Toolkit / PERFORM documentation DOIs and Kaggle dataset pages as appropriate. Keep license attribution for CC-BY materials.
EOF

cat << 'EOF' > "$ROOT/$CASE1/requirements.txt"
# Stream 1 — Energy Systems & Environmental Modeling
# Autonomous Grid-Balancing Agent for Renewable Wind Integration
numpy>=1.24
pandas>=2.0
scipy>=1.10
matplotlib>=3.7
pypsa>=0.27
networkx>=3.0
boto3>=1.28
h5py>=3.8
xarray>=2023.1
scikit-learn>=1.3
python-dotenv>=1.0
EOF

cat << 'EOF' > "$ROOT/$CASE1/agent_starter.py"
#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Grid-Balancing Agent for Renewable Wind Integration

This skeleton implements a minimal perceive -> reason -> act loop.
Replace TODOs with your forecast models, PyPSA optimization, and policies.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class GridObservation:
    timestamps: pd.DatetimeIndex
    load_mw: np.ndarray
    wind_mw: np.ndarray

    @property
    def net_load_mw(self) -> np.ndarray:
        return self.load_mw - self.wind_mw


@dataclass
class AgentAction:
    storage_charge_mw: np.ndarray
    curtail_wind_mw: np.ndarray
    notes: str


def perceive(load_csv: Path, wind_csv: Path | None = None) -> GridObservation:
    """Load local CSV time series. See data/README.md for download instructions."""
    if not load_csv.exists():
        raise FileNotFoundError(
            f"Missing {load_csv}. Download a load series per data/README.md "
            "(e.g., Kaggle PJM hourly or PERFORM ISO load)."
        )

    load_df = pd.read_csv(load_csv)
    # Heuristic: first datetime-like column + first numeric MW column
    time_col = load_df.columns[0]
    value_col = load_df.select_dtypes(include="number").columns[0]
    load_df[time_col] = pd.to_datetime(load_df[time_col])
    load_df = load_df.sort_values(time_col)

    load_mw = load_df[value_col].to_numpy(dtype=float)

    if wind_csv and wind_csv.exists():
        wind_df = pd.read_csv(wind_csv)
        w_time = wind_df.columns[0]
        w_val = wind_df.select_dtypes(include="number").columns[0]
        wind_df[w_time] = pd.to_datetime(wind_df[w_time])
        wind_df = wind_df.sort_values(w_time)
        wind_mw = wind_df[w_val].to_numpy(dtype=float)
        n = min(len(load_mw), len(wind_mw))
        load_mw, wind_mw = load_mw[:n], wind_mw[:n]
        timestamps = pd.DatetimeIndex(load_df[time_col].iloc[:n])
    else:
        # Synthetic wind placeholder so the loop runs before real WTK data arrives
        rng = np.random.default_rng(42)
        wind_mw = np.clip(0.35 * load_mw + rng.normal(0, 0.05 * np.nanmean(load_mw), size=len(load_mw)), 0, None)
        timestamps = pd.DatetimeIndex(load_df[time_col])
        print("[warn] No wind CSV provided — using synthetic wind. Replace with NREL WTK/PERFORM data.")

    return GridObservation(timestamps=timestamps, load_mw=load_mw, wind_mw=wind_mw)


def reason(obs: GridObservation) -> dict[str, Any]:
    """TODO: replace with ML forecast + uncertainty / risk scoring."""
    net = obs.net_load_mw
    return {
        "mean_net_load_mw": float(np.nanmean(net)),
        "peak_net_load_mw": float(np.nanmax(net)),
        "wind_capacity_factor": float(np.nanmean(obs.wind_mw) / (np.nanmax(obs.wind_mw) + 1e-9)),
        "imbalance_proxy_mwh": float(np.nansum(np.abs(net - np.nanmean(net)))),
    }


def act(obs: GridObservation, plan: dict[str, Any]) -> AgentAction:
    """
    Naive policy: charge storage when wind > load, curtail excess beyond storage rate.
    TODO: replace with PyPSA LOPF / multi-period storage optimization.
    """
    # Optional PyPSA import for teams ready to wire a real network model
    try:
        import pypsa  # noqa: F401

        pypsa_available = True
    except ImportError:
        pypsa_available = False

    surplus = obs.wind_mw - obs.load_mw
    charge = np.clip(surplus, 0, None) * 0.5
    curtail = np.clip(surplus - charge, 0, None)
    note = (
        f"naive storage policy | peak_net={plan['peak_net_load_mw']:.1f} MW | "
        f"pypsa_installed={pypsa_available}"
    )
    return AgentAction(storage_charge_mw=charge, curtail_wind_mw=curtail, notes=note)


def evaluate(obs: GridObservation, action: AgentAction) -> dict[str, float]:
    # Convention: positive residual = unmet demand after usable wind and storage charge.
    usable_wind = obs.wind_mw - action.curtail_wind_mw
    residual = obs.load_mw - usable_wind + action.storage_charge_mw
    return {
        "mean_abs_residual_mw": float(np.nanmean(np.abs(residual))),
        "total_curtail_mwh": float(np.nansum(action.curtail_wind_mw)),
        "total_charge_mwh": float(np.nansum(action.storage_charge_mw)),
    }


def run_agent_loop(obs: GridObservation, max_iters: int = 2) -> None:
    best = None
    for i in range(1, max_iters + 1):
        plan = reason(obs)
        action = act(obs, plan)
        metrics = evaluate(obs, action)
        print(f"=== iteration {i} ===")
        print("plan:", plan)
        print("action:", action.notes)
        print("metrics:", metrics)
        best = metrics
        # TODO: revise policy parameters from metrics (true autonomy)
    print("final:", best)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 1 grid-balancing starter agent")
    parser.add_argument(
        "--load-csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "load.csv",
        help="Path to load time-series CSV",
    )
    parser.add_argument("--wind-csv", type=Path, default=None, help="Optional wind power CSV")
    parser.add_argument("--iters", type=int, default=2)
    args = parser.parse_args()

    # If no user data yet, synthesize a tiny demo series so `python agent_starter.py` runs
    if not args.load_csv.exists():
        args.load_csv.parent.mkdir(parents=True, exist_ok=True)
        demo = pd.DataFrame(
            {
                "Datetime": pd.date_range("2018-01-01", periods=168, freq="h"),
                "Load_MW": 800 + 120 * np.sin(np.linspace(0, 6 * np.pi, 168)) + np.random.default_rng(0).normal(0, 20, 168),
            }
        )
        demo.to_csv(args.load_csv, index=False)
        print(f"[info] Wrote demo load CSV to {args.load_csv}")

    obs = perceive(args.load_csv, args.wind_csv)
    run_agent_loop(obs, max_iters=args.iters)


if __name__ == "__main__":
    main()
EOF

# =============================================================================
# STREAM 2 — Applied Physics, Aerospace & Electrical Engineering
# =============================================================================
CASE2="02-applied-physics-aerospace-electrical/Case 1 - Autonomous Structural-Health and Aerodynamic-Design Agent"

cat << 'EOF' > "$ROOT/$CASE2/README.md"
# Case 1 — Autonomous Structural-Health and Aerodynamic-Design Agent

**Stream:** Applied Physics, Aerospace & Electrical Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Aerospace assets degrade under complex thermo-mechanical and aerodynamic loads. Predicting **Remaining Useful Life (RUL)** for turbofan engines from multi-sensor streams — and optionally coupling that to aerodynamic design feedback — is a classic hard-science PHM (prognostics and health management) problem.

**Your challenge:** Build an **autonomous agent** that monitors engine sensor trajectories, diagnoses degradation modes, predicts RUL, and iteratively proposes maintenance / operating / design actions evaluated against quantitative aerospace metrics — not a static notebook with a single offline fit.

---

## Industrial Significance

- Unplanned engine removals and in-flight shutdowns drive airline cost, safety risk, and fleet availability.
- NASA’s C-MAPSS turbofan datasets are the community benchmark for data-driven prognostics used across industry and academia.
- Combining structural health signals with aerodynamic performance (lift/drag, high-lift behavior) mirrors digital-twin ambitions in aerospace OEMs and MRO providers.
- Alberta’s growing aerospace / UAV / energy-turbomachinery ecosystem benefits from transferable PHM agent patterns.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest NASA C-MAPSS multivariate sensor time series (FD001–FD004) with operational settings.
2. **Diagnose:** Infer health indices / fault progression under one or more operating conditions and fault modes.
3. **Predict:** Estimate RUL on held-out test trajectories with calibrated uncertainty.
4. **Act & Iterate:** Agent proposes inspection thresholds, derate schedules, or (stretch) aerodynamic geometry tweaks; re-evaluate against RUL / performance metrics.
5. **Stretch — Aero:** Use force/moment CSVs from NVIDIA HiLiftAeroML (NASA CRM high-lift) to train a surrogate and let the agent search geometry / AoA trade-offs offline (full volume CFD is too large to download wholesale — use metadata + force files).

---

## Recommended Agent Architecture & Starter Code Pointers

```
Sensors / AoA,geo  ->  Health encoder  ->  RUL / aero surrogate  ->  Action policy
         ^                         |                    |
         +----- re-simulate / re-score after action ----+
```

**Starter frameworks (open source):**
- NASA [C-MAPSS Jet Engine Simulated Data](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data)
- scikit-learn / PyTorch / [sktime](https://www.sktime.net/) for time-series prognostics
- Stretch aero: [HiLiftAeroML on Hugging Face](https://huggingface.co/datasets/nvidia/HiLiftAeroML) (CC-BY-4.0) — download **force_mom_*.csv** subsets only
- Optional CAD/CFD tools: OpenVSP, XFOIL, SU2 (for teams with aero expertise)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
pip install -r requirements.txt
python agent_starter.py --help
```

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| RUL RMSE / MAE (cycles) | Report on FD001 (baseline) and optionally harder FD002–FD004 |
| Prognostic Horizon / Timeliness | Prefer early, calibrated warnings over late overconfident ones |
| Score vs. PHM challenge-style asymmetric penalties | Optional; document if used |
| Aero stretch: force prediction MAE on Cl/Cd | If using HiLiftAeroML force CSVs |
| Autonomy | Closed-loop propose → evaluate → revise on at least one held-out engine |
| Practicality | Demo trains/infers within hackathon compute limits |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
EOF

cat << 'EOF' > "$ROOT/$CASE2/data/README.md"
# Data Guide — Structural-Health & Aerodynamic-Design Agent (Stream 2)

---

## Primary Dataset: NASA C-MAPSS Turbofan Engine Degradation

- **Portal:** https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
- **Also mirrored on:** IEEE DataPort, Kaggle, Hugging Face community mirrors  
- **Format:** Space-separated text files (`.txt`) inside a zip; 26 columns per row  
- **Subsets:** FD001, FD002, FD003, FD004 (increasing operating-condition / fault-mode complexity)

### Column Schema (per row)

| Index | Field |
|---|---|
| 1 | Unit / engine ID |
| 2 | Time (cycles) |
| 3–5 | Operational settings 1–3 |
| 6–26 | Sensor measurements 1–21 |

Training trajectories run to failure; test trajectories end before failure. True RUL vectors are provided for test engines (`RUL_FD00x.txt`).

### Subset Complexity

| Set | Train / Test engines | Conditions | Fault modes |
|---|---|---|---|
| FD001 | 100 / 100 | 1 (sea level) | 1 (HPC degradation) |
| FD002 | 260 / 259 | 6 | 1 |
| FD003 | 100 / 100 | 1 | 2 (HPC + Fan) |
| FD004 | 248 / 249 | 6 | 2 |

### Download

```bash
mkdir -p raw/cmapss
# Prefer the NASA Open Data Portal download page, then unzip into raw/cmapss/
# Example if you have a direct zip URL or local copy:
# unzip CMAPSSData.zip -d raw/cmapss
```

**Hugging Face convenience mirror (community; verify integrity against NASA):**

```bash
pip install datasets
python -c "from datasets import load_dataset; print(load_dataset('SoyVitou/NASA-C-MAPSS-Turbofan-Engine', 'FD001'))"
```

### Loading Example

```python
import pandas as pd

cols = ["unit", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]
train = pd.read_csv("raw/cmapss/train_FD001.txt", sep=r"\s+", header=None, names=cols)
print(train.head())
```

---

## Stretch Dataset: NVIDIA HiLiftAeroML (NASA CRM High-Lift CFD)

- **Hugging Face:** https://huggingface.co/datasets/nvidia/HiLiftAeroML  
- **Paper:** https://doi.org/10.48550/arxiv.2605.19565  
- **License:** CC-BY-4.0  
- **Content:** 1,800 WMLES samples (180 geometry variants × 10 AoA); geometries + volume/surface fields + integral forces  
- **Warning:** Full repo is on the order of **tens of TB**. For the hackathon, download **only** metadata / `force_mom_*.csv` files.

```bash
pip install huggingface_hub
hf download nvidia/HiLiftAeroML --repo-type dataset --local-dir raw/hilift \
  --include "*/force_mom_*.csv" --include "geo_values_all.csv"
```

Force CSVs typically include time-averaged drag, lift, moment, and pressure/viscous coefficient integrals — ideal for surrogate modeling without staging volume fields.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── cmapss/
    └── hilift/   # optional stretch
```
EOF

cat << 'EOF' > "$ROOT/$CASE2/requirements.txt"
# Stream 2 — Applied Physics, Aerospace & Electrical Engineering
# Requires Python 3.10+
numpy>=1.24
pandas>=2.0
scipy>=1.10
matplotlib>=3.7
scikit-learn>=1.3
huggingface_hub>=0.20
datasets>=2.16
# Optional stretch: torch>=2.0, sktime>=0.24
EOF

cat << 'EOF' > "$ROOT/$CASE2/agent_starter.py"
#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 2 Starter Agent
Case: Autonomous Structural-Health and Aerodynamic-Design Agent

Minimal RUL baseline on NASA C-MAPSS-style tables + iterative threshold policy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


COLS = ["unit", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]


def synthesize_cmapss_like(path: Path, n_units: int = 20, max_cycles: int = 200) -> Path:
    """Create a tiny synthetic FD001-like table so the starter runs without NASA zip."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    rows = []
    for u in range(1, n_units + 1):
        life = int(rng.integers(120, max_cycles))
        for c in range(1, life + 1):
            health = 1.0 - c / life
            sensors = 500 + 50 * health + rng.normal(0, 3, size=21)
            ops = rng.normal(0, 1, size=3)
            rows.append([u, c, *ops, *sensors])
    df = pd.DataFrame(rows, columns=COLS)
    df.to_csv(path, sep=" ", header=False, index=False)
    print(f"[info] Wrote synthetic C-MAPSS-like training data to {path}")
    return path


def load_train(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=r"\s+", header=None, names=COLS)
    max_cycle = df.groupby("unit")["cycle"].transform("max")
    df["rul"] = max_cycle - df["cycle"]
    return df


def perceive(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    feature_cols = [c for c in df.columns if c.startswith("op") or c.startswith("s")]
    X = df[feature_cols].to_numpy()
    y = df["rul"].to_numpy()
    return X, y


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    metrics = {
        "mae": float(mean_absolute_error(yte, pred)),
        "rmse": float(mean_squared_error(yte, pred) ** 0.5),
    }
    return model, metrics


def act(predicted_rul: np.ndarray, inspect_threshold: float) -> dict:
    """Policy: flag engines/cycles below RUL threshold for inspection."""
    alerts = predicted_rul < inspect_threshold
    return {
        "threshold_cycles": inspect_threshold,
        "alert_rate": float(np.mean(alerts)),
        "n_alerts": int(np.sum(alerts)),
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    X, y = perceive(df)
    model, metrics = reason_train(X, y)
    print("baseline_metrics:", metrics)
    pred = model.predict(X)
    threshold = float(np.percentile(y, 20))
    for i in range(1, iters + 1):
        decision = act(pred, threshold)
        # Autonomous revision: tighten threshold if alert rate too low / high
        if decision["alert_rate"] < 0.05:
            threshold *= 1.1
        elif decision["alert_rate"] > 0.35:
            threshold *= 0.9
        print(f"=== iteration {i} ===", decision, f"next_threshold={threshold:.1f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 2 SHM / RUL starter agent")
    parser.add_argument(
        "--train-file",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "cmapss" / "train_FD001.txt",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    if not args.train_file.exists():
        synthesize_cmapss_like(args.train_file)

    df = load_train(args.train_file)
    run_loop(df, iters=args.iters)
    print("TODO: swap synthetic/local file for official NASA C-MAPSS FD001–FD004.")
    print("TODO: stretch — consume HiLiftAeroML force_mom CSVs for aero surrogates.")


if __name__ == "__main__":
    main()
EOF

# =============================================================================
# STREAM 3 — Software, Cryptography & Computational Math
# =============================================================================
CASE3="03-software-cryptography-computational-math/Case 1 - Autonomous Quantum-Safe Cryptography Migration Agent"

cat << 'EOF' > "$ROOT/$CASE3/README.md"
# Case 1 — Autonomous Quantum-Safe Cryptography Migration Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Cryptographically relevant quantum computers threaten RSA/ECC. NIST has finalized post-quantum standards (**FIPS 203 ML-KEM**, **FIPS 204 ML-DSA**, **FIPS 205 SLH-DSA**). Enterprises must inventory quantum-vulnerable cryptography and plan sequenced migrations under dependency, budget, and downtime constraints — a combinatorial planning problem, not a slide deck.

**Your challenge:** Build an **autonomous agent** that discovers classical crypto usage (code / CBOM / synthetic estate graphs), maps findings to NIST PQC replacements, simulates migration waves, and iteratively repairs plans against failure modes — beyond “chat about Kyber.”

---

## Industrial Significance

- CNSA 2.0 / federal and critical-infrastructure timelines make PQC migration a dated compliance requirement.
- Real crypto inventories are sensitive; synthetic estates (AutoPQC) enable reproducible research without leaking attack maps.
- Incorrect migrations fail in subtle ways (header limits, hybrid negotiation, performance regressions) — see PQC-MFB failure families.
- Canadian critical infrastructure and Alberta energy/OT environments increasingly need crypto-agility roadmaps.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest a synthetic cryptographic estate or scan a sample codebase for RSA/ECC/TLS usage.
2. **Classify:** Map each finding to NIST FIPS 203/204/205 algorithms and risk tiers.
3. **Plan:** Produce a staged migration schedule respecting dependencies and budgets (QUBO / ILP / heuristic planner).
4. **Validate:** Benchmark candidate KEMs/signatures via liboqs / `oqs` Python bindings; score plans against PQC-MFB-style failure checks where applicable.
5. **Iterate:** Agent revises the plan when simulations detect dependency violations, over-budget stages, or known failure families.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Inventory / CBOM -> Risk graph -> Migration planner -> liboqs benchmarks -> Revised plan
```

**Starter frameworks (open source):**
- NIST PQC standards: https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- [Open Quantum Safe liboqs](https://github.com/open-quantum-safe/liboqs) + `oqs` Python package
- [pqc-migrator](https://github.com/BasitS-hash/pqc-migrator) — readiness scanner / CBOM
- [AutoPQC planner](https://github.com/srikanthlumen-bot/autopqc-planner) + IEEE DataPort synthetic estates
- [PQC-MFB](https://huggingface.co/datasets/nickh007/pqc-mfb) — migration failure benchmark
- Optional: [Qiskit](https://github.com/Qiskit/qiskit) for didactic Shor-threat demonstrations (not a substitute for PQC engineering)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
pip install -r requirements.txt
python agent_starter.py --help
```

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Inventory coverage | % of synthetic estate nodes classified with NIST mapping |
| Plan feasibility | Zero dependency violations; stages within budget |
| Risk coverage | Stages to ≥90% risk reduction (AutoPQC-style) |
| Crypto performance | ML-KEM / ML-DSA handshake or encapsulate latency vs. classical baseline (liboqs) |
| Failure awareness | Explicit checks against ≥1 PQC-MFB failure family |
| Autonomy | Planner revises after simulated constraint violation |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
EOF

cat << 'EOF' > "$ROOT/$CASE3/data/README.md"
# Data Guide — Quantum-Safe Cryptography Migration Agent (Stream 3)

---

## 1. NIST Post-Quantum Standards (normative references)

| FIPS | Algorithm | Role |
|---|---|---|
| FIPS 203 | ML-KEM (Kyber) | Key encapsulation / general encryption |
| FIPS 204 | ML-DSA (Dilithium) | Primary digital signatures |
| FIPS 205 | SLH-DSA (SPHINCS+) | Stateless hash-based signatures |

- Announcement: https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- Transition guidance: NIST IR 8547 (search on csrc.nist.gov)

These are **specifications**, not tabular ML datasets — your agent should encode their parameter sets and migration mappings.

---

## 2. AutoPQC — Synthetic Enterprise Cryptographic Estates

- **IEEE DataPort:** https://ieee-dataport.org/documents/autopqc-synthetic-enterprise-cryptographic-estates-and-post-quantum-migration-planning  
- **Code:** https://github.com/srikanthlumen-bot/autopqc-planner  
- **Why synthetic:** Real enterprise crypto graphs are confidential (they are attacker roadmaps).
- **Contents:** Seeded, reproducible estate generators + migration-planning benchmark results (`results_tight.json`, `results_loose.json`) under multiple planners/baselines.
- **Formats:** Python generator scripts + JSON result files; estates reconstructed from seeds.

```bash
git clone https://github.com/srikanthlumen-bot/autopqc-planner.git raw/autopqc-planner
cd raw/autopqc-planner
# Follow repo README to generate estates from seeds and reproduce planning baselines.
```

---

## 3. PQC-MFB — Post-Quantum Migration Failure Benchmark

- **Dataset:** https://huggingface.co/datasets/nickh007/pqc-mfb  
- **Tooling:** https://github.com/nickharris808/pqc-mfb  
- **What:** 322 cases across 39 failure families for scoring migration robustness.
- **Format:** Structured benchmark records (see HF dataset card) + Python scorer.

```bash
pip install datasets
python -c "from datasets import load_dataset; ds=load_dataset('nickh007/pqc-mfb'); print(ds)"
```

---

## 4. Sample Inventory for Local Hacking (bundled schema)

Create your own JSON CBOM-like inventory if AutoPQC clone is slow:

```json
{
  "assets": [
    {"id": "api-gateway", "algo": "RSA-2048", "protocol": "TLS", "criticality": "high", "deps": ["hsm-1"]},
    {"id": "hsm-1", "algo": "ECDSA-P256", "protocol": "signing", "criticality": "critical", "deps": []},
    {"id": "iot-fleet", "algo": "ECDH-P256", "protocol": "MQTT-TLS", "criticality": "medium", "deps": ["api-gateway"]}
  ]
}
```

Suggested path: `data/raw/sample_estate.json` (the starter agent can generate this automatically).

---

## Mapping Cheat Sheet

| Classical | Risk | NIST-oriented replacement |
|---|---|---|
| RSA key transport / TLS KX | Critical | ML-KEM-768 (often hybrid with X25519 during transition) |
| ECDSA / RSA signatures | High | ML-DSA (Dilithium) or SLH-DSA where hash-based is required |
| ECDH | Critical | ML-KEM / hybrid KEM |

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── sample_estate.json
    ├── autopqc-planner/
    └── pqc-mfb/
```
EOF

cat << 'EOF' > "$ROOT/$CASE3/requirements.txt"
# Stream 3 — Software, Cryptography & Computational Math
numpy>=1.24
pandas>=2.0
networkx>=3.0
pyyaml>=6.0
cryptography>=41.0
# Optional: pip install oqs  (Open Quantum Safe Python bindings; may need liboqs system libs)
# Optional: qiskit>=1.0
huggingface_hub>=0.20
datasets>=2.16
python-dotenv>=1.0
EOF

cat << 'EOF' > "$ROOT/$CASE3/agent_starter.py"
#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous Quantum-Safe Cryptography Migration Agent
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import networkx as nx


NIST_MAP = {
    "RSA-2048": {"fips": "FIPS 203/204", "pqc": "ML-KEM-768 + ML-DSA-65", "priority": 1},
    "RSA-4096": {"fips": "FIPS 203/204", "pqc": "ML-KEM-1024 + ML-DSA-87", "priority": 1},
    "ECDSA-P256": {"fips": "FIPS 204", "pqc": "ML-DSA-65", "priority": 1},
    "ECDH-P256": {"fips": "FIPS 203", "pqc": "ML-KEM-768 (hybrid X25519+ML-KEM)", "priority": 1},
    "AES-256-GCM": {"fips": "symmetric OK", "pqc": "retain (increase key agility)", "priority": 3},
}


def write_sample_estate(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    estate = {
        "assets": [
            {"id": "api-gateway", "algo": "RSA-2048", "protocol": "TLS", "criticality": "high", "deps": ["hsm-1"]},
            {"id": "hsm-1", "algo": "ECDSA-P256", "protocol": "signing", "criticality": "critical", "deps": []},
            {"id": "iot-fleet", "algo": "ECDH-P256", "protocol": "MQTT-TLS", "criticality": "medium", "deps": ["api-gateway"]},
            {"id": "data-lake", "algo": "AES-256-GCM", "protocol": "at-rest", "criticality": "high", "deps": ["hsm-1"]},
            {"id": "legacy-vpn", "algo": "RSA-4096", "protocol": "IKE", "criticality": "high", "deps": ["api-gateway"]},
        ]
    }
    path.write_text(json.dumps(estate, indent=2), encoding="utf-8")
    print(f"[info] Wrote sample estate to {path}")


def perceive(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_graph(estate: dict[str, Any]) -> nx.DiGraph:
    g = nx.DiGraph()
    for asset in estate["assets"]:
        g.add_node(asset["id"], **asset)
        for dep in asset.get("deps", []):
            g.add_edge(asset["id"], dep)  # migrate dependencies first
    return g


def reason(g: nx.DiGraph) -> list[dict[str, Any]]:
    findings = []
    for node, data in g.nodes(data=True):
        algo = data.get("algo", "")
        mapping = NIST_MAP.get(algo, {"fips": "unknown", "pqc": "manual review", "priority": 2})
        findings.append({"id": node, "algo": algo, **mapping, "criticality": data.get("criticality")})
    findings.sort(key=lambda x: (x["priority"], 0 if x["criticality"] == "critical" else 1))
    return findings


def act(g: nx.DiGraph, findings: list[dict[str, Any]], budget_per_stage: int = 2) -> list[list[str]]:
    """Greedy wave planner: migrate dependency sinks first, then higher priority."""
    priority = {f["id"]: f["priority"] for f in findings}
    candidates = {n for n in g.nodes if priority.get(n, 99) <= 2}
    if nx.is_directed_acyclic_graph(g):
        topo = list(reversed(list(nx.topological_sort(g))))
    else:
        topo = list(g.nodes)
    topo_index = {n: i for i, n in enumerate(topo)}

    stages: list[list[str]] = []
    migrated: set[str] = set()
    remaining = set(candidates)
    while remaining:
        ready = [n for n in remaining if set(g.successors(n)).issubset(migrated)]
        if not ready:
            ready = [min(remaining, key=lambda n: (priority.get(n, 99), topo_index.get(n, 10**9)))]
        ready.sort(key=lambda n: (priority.get(n, 99), topo_index.get(n, 10**9)))
        stage = ready[:budget_per_stage]
        stages.append(stage)
        migrated.update(stage)
        remaining -= set(stage)
    return stages


def evaluate(stages: list[list[str]], g: nx.DiGraph) -> dict[str, Any]:
    migrated: set[str] = set()
    violations = 0
    for stage in stages:
        for node in stage:
            deps = set(g.successors(node))
            if not deps.issubset(migrated):
                violations += 1
        migrated.update(stage)
    return {"n_stages": len(stages), "dependency_violations": violations, "coverage": len(migrated) / max(len(g), 1)}

def run_loop(estate_path: Path, iters: int = 3) -> None:
    estate = perceive(estate_path)
    g = build_graph(estate)
    findings = reason(g)
    budget = 2
    for i in range(1, iters + 1):
        stages = act(g, findings, budget_per_stage=budget)
        metrics = evaluate(stages, g)
        print(f"=== iteration {i} ===")
        print("findings:", json.dumps(findings, indent=2))
        print("stages:", stages)
        print("metrics:", metrics)
        # Autonomous repair: if violations, shrink stage size (stricter sequencing)
        if metrics["dependency_violations"] > 0 and budget > 1:
            budget -= 1
            print(f"[revise] reducing budget_per_stage -> {budget}")
        else:
            break
    print("TODO: integrate liboqs benchmarks and AutoPQC / PQC-MFB scorers.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 3 PQC migration starter agent")
    parser.add_argument(
        "--estate",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "sample_estate.json",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    if not args.estate.exists():
        write_sample_estate(args.estate)
    run_loop(args.estate, iters=args.iters)


if __name__ == "__main__":
    main()
EOF

# =============================================================================
# STREAM 4 — Materials Science & Chemical Synthesis
# =============================================================================
CASE4="04-materials-science-chemical-synthesis/Case 1 - Autonomous Battery Cathode Discovery Agent"

cat << 'EOF' > "$ROOT/$CASE4/README.md"
# Case 1 — Autonomous Battery Cathode Discovery Agent

**Stream:** Materials Science & Chemical Synthesis  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Discovering battery electrode materials requires navigating a vast chemical space under competing objectives: voltage, gravimetric/volumetric capacity, energy density, thermodynamic stability, earth abundance, and toxicity. Manual browsing of databases does not scale.

**Your challenge:** Build an **autonomous materials agent** that queries the Materials Project, proposes cathode / insertion-electrode candidates, scores multi-objective trade-offs, and iteratively refines search constraints using `pymatgen` / `mp-api` — a closed discovery loop, not a one-shot chatbot answer.

---

## Industrial Significance

- Electrification of transport and grid storage depends on better, cheaper, more sustainable cathodes.
- High-throughput DFT databases (Materials Project) already encode thousands of insertion electrodes ready for ML + agentic search.
- Alberta’s energy transition and Canada’s critical-minerals strategy make battery materials R&D regionally strategic.
- Agents that respect stability and resource constraints reduce wasted wet-lab cycles.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Pull insertion-electrode documents via Materials Project API (`mp-api`) — voltage, capacity, energy density, working ion, stability proxies.
2. **Featurize:** Use `pymatgen` structures / compositions for descriptors (elemental properties, structural fingerprints).
3. **Search:** Multi-objective selection (e.g., Pareto front on energy density vs. stability vs. critical-element penalties).
4. **Act & Iterate:** Agent updates query filters / generative proposals based on scored shortlists; optional MatGL property models for surrogates.
5. **Report:** Ranked candidates with MP IDs, predicted metrics, and rationale suitable for a materials engineer.

---

## Recommended Agent Architecture & Starter Code Pointers

```
MP API query -> pymatgen featurize -> multi-objective rank -> constraint update -> re-query
```

**Starter frameworks (open source):**
- [Materials Project API docs](https://docs.materialsproject.org/downloading-data/using-the-api/getting-started)
- [`mp-api`](https://github.com/materialsproject/api) / `MPRester`
- [`pymatgen`](https://github.com/materialsproject/pymatgen)
- Optional: [MatGL](https://github.com/materialsvirtuallab/matgl) graph deep learning; ASE for atomistic workflows

**API key:** Free Materials Project account → dashboard API key. Export as `MP_API_KEY`.

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
export MP_API_KEY=your_key_here   # Windows PowerShell: $env:MP_API_KEY="..."
pip install -r requirements.txt
python agent_starter.py --help
```

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Candidate quality | Shortlist with energy density / voltage / capacity reported from MP fields |
| Stability filter | Prefer electrodes within documented stability windows when available |
| Critical element penalty | Explicit scoring for Co/Ni/etc. abundance or supply-risk heuristics |
| Pareto coverage | Non-dominated set size and diversity across chemistries |
| Autonomy | ≥1 iteration where filters change based on prior shortlist statistics |
| Reproducibility | Seeded queries + saved JSON shortlist artifacts |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
EOF

cat << 'EOF' > "$ROOT/$CASE4/data/README.md"
# Data Guide — Battery Cathode Discovery Agent (Stream 4)

---

## Primary Source: Materials Project Insertion Electrodes

- **API getting started:** https://docs.materialsproject.org/downloading-data/using-the-api/getting-started  
- **Battery Explorer (UI):** https://next-gen.materialsproject.org/  
- **Endpoint used in docs/community:** `materials.insertion_electrodes` via `mp_api.client.MPRester`  
- **Scale:** On the order of **6,800+** battery / insertion-electrode entries exposed through the Battery Explorer / API (count evolves with MP releases)  
- **Formats:** JSON documents via API (convertible to CSV/Parquet locally); structures as CIF / pymatgen `Structure`

### Important fields (typical)

| Field | Meaning | Units (typical) |
|---|---|---|
| `battery_id` / material ids | MP identifiers | — |
| `average_voltage` | Average voltage | V |
| `capacity_grav` | Gravimetric capacity | mAh/g |
| `capacity_vol` | Volumetric capacity | mAh/cm³ |
| `energy_grav` | Specific energy | Wh/kg |
| `energy_vol` | Energy density | Wh/L |
| `working_ion` | e.g. Li, Na, Mg | — |
| stability / framwork fields | Stability proxies | MP-specific |

Exact field names can vary slightly by client version — inspect returned documents and select `fields=[...]` explicitly.

### Setup

1. Create a free account at https://next-gen.materialsproject.org/  
2. Copy your API key from the dashboard  
3. Export it:

```bash
export MP_API_KEY="YOUR_KEY"
```

### Download / query example

```python
from mp_api.client import MPRester
import pandas as pd
import os

with MPRester(os.environ["MP_API_KEY"], use_document_model=False) as mpr:
    docs = mpr.materials.insertion_electrodes.search(
        working_ion="Li",
        # optional filters, e.g. average_voltage=(3.0, 4.5)
    )

df = pd.DataFrame(docs)
df.to_csv("raw/mp_li_insertion_electrodes.csv", index=False)
print(len(df), "electrodes cached")
```

Community snippet (full pull — can be large/slow):

```python
with MPRester(use_document_model=False) as mpr:
    elec_docs = mpr.materials.insertion_electrodes.search()
```

---

## Offline Hackathon Fallback

If API access is limited during the event, cache a filtered CSV on Saturday morning and commit **only** a small sample (tens–hundreds of rows) plus the download script. Do not commit the entire MP dump.

The starter agent ships a **tiny synthetic electrode table** so pipelines run before the API key is configured.

---

## Related Structure Data

For composition/structure featurization, query materials by `material_ids` returned on electrode docs and load structures through pymatgen:

```python
from pymatgen.core import Structure
# structure = mpr.get_structure_by_material_id("mp-XXXX")
```

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── mp_li_insertion_electrodes.csv
    └── sample_electrodes.csv   # optional tiny cache
```

### Citation

Acknowledge the Materials Project and cite relevant MP / pymatgen publications when presenting.
EOF

cat << 'EOF' > "$ROOT/$CASE4/requirements.txt"
# Stream 4 — Materials Science & Chemical Synthesis
numpy>=1.24
pandas>=2.0
scipy>=1.10
matplotlib>=3.7
pymatgen>=2023.0
mp-api>=0.41
python-dotenv>=1.0
# Optional: matgl, ase
EOF

cat << 'EOF' > "$ROOT/$CASE4/agent_starter.py"
#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 4 Starter Agent
Case: Autonomous Battery Cathode Discovery Agent
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd


def synthetic_electrodes(path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(3)
    chem = ["NMC811", "NCA", "LFP", "LMO", "NMC622", "LNMO", "NaFePO4", "Li2MnO3"]
    rows = []
    for i, name in enumerate(chem * 5):
        rows.append(
            {
                "battery_id": f"synth-{i}-{name}",
                "formula": name,
                "working_ion": "Li" if "Na" not in name else "Na",
                "average_voltage": float(rng.uniform(2.8, 4.6)),
                "capacity_grav": float(rng.uniform(100, 220)),
                "energy_grav": float(rng.uniform(300, 800)),
                "stability_proxy": float(rng.uniform(0.0, 0.12)),
                "contains_co": int("NMC" in name or "NCA" in name),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote synthetic electrode table to {path}")
    return df


def try_fetch_mp(limit: int = 50) -> pd.DataFrame | None:
    key = os.environ.get("MP_API_KEY")
    if not key:
        print("[warn] MP_API_KEY not set — using local/synthetic data.")
        return None
    try:
        from mp_api.client import MPRester
    except ImportError:
        print("[warn] mp-api not installed.")
        return None

    with MPRester(key, use_document_model=False) as mpr:
        docs = mpr.materials.insertion_electrodes.search(working_ion="Li", num_chunks=1, chunk_size=limit)
    return pd.DataFrame(docs)


def perceive(csv_path: Path) -> pd.DataFrame:
    mp_df = try_fetch_mp()
    if mp_df is not None and len(mp_df) > 0:
        return mp_df
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return synthetic_electrodes(csv_path)


def score(df: pd.DataFrame, co_penalty: float = 50.0) -> pd.DataFrame:
    out = df.copy()
    # Flexible column picking for MP vs synthetic
    energy = None
    for c in ["energy_grav", "energy_density", "specific_energy"]:
        if c in out.columns:
            energy = out[c].astype(float)
            break
    if energy is None and {"average_voltage", "capacity_grav"}.issubset(out.columns):
        energy = out["average_voltage"].astype(float) * out["capacity_grav"].astype(float)
    if energy is None:
        raise ValueError("Could not find energy-related columns to score.")

    stab = out["stability_proxy"] if "stability_proxy" in out.columns else 0.0
    co = out["contains_co"] if "contains_co" in out.columns else 0.0
    out["agent_score"] = energy - 500.0 * pd.Series(stab).astype(float) - co_penalty * pd.Series(co).astype(float)
    return out.sort_values("agent_score", ascending=False)


def act(shortlist: pd.DataFrame, voltage_min: float) -> dict:
    if "average_voltage" in shortlist.columns:
        filtered = shortlist[shortlist["average_voltage"] >= voltage_min]
    else:
        filtered = shortlist
    return {
        "voltage_min": voltage_min,
        "n_candidates": int(len(filtered)),
        "top_ids": filtered.head(5).get("battery_id", filtered.head(5).iloc[:, 0]).astype(str).tolist(),
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    voltage_min = 3.2
    for i in range(1, iters + 1):
        ranked = score(df)
        decision = act(ranked, voltage_min)
        print(f"=== iteration {i} ===", decision)
        print(ranked.head(3)[["battery_id", "agent_score"]].to_string(index=False) if "battery_id" in ranked.columns else ranked.head(3))
        # Autonomous revise: if too many candidates, raise voltage floor
        if decision["n_candidates"] > 20:
            voltage_min += 0.1
            print(f"[revise] voltage_min -> {voltage_min:.2f}")
        elif decision["n_candidates"] < 3:
            voltage_min = max(2.5, voltage_min - 0.1)
            print(f"[revise] voltage_min -> {voltage_min:.2f}")
        else:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 4 cathode discovery starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "sample_electrodes.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)
    print("TODO: add pymatgen composition featurization and MatGL surrogates.")


if __name__ == "__main__":
    main()
EOF

# =============================================================================
# STREAM 5 — Life Sciences & Bio-Engineering
# =============================================================================
CASE5="05-life-sciences-bio-engineering/Case 1 - Autonomous Protein-Structure-to-Toxicity Screening Agent"

cat << 'EOF' > "$ROOT/$CASE5/README.md"
# Case 1 — Autonomous Protein-Structure-to-Toxicity Screening Agent

**Stream:** Life Sciences & Bio-Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Toxicological profiling of new compounds still bottlenecks drug and chemical development. Modern pipelines can close a **wet-lab ↔ dry-lab loop**: structural biology context (PDB / AlphaFold) informs target relevance, while high-throughput screens (Tox21 / ToxCast) provide bioactivity labels for predictive models.

**Your challenge:** Build an **autonomous agent** that retrieves protein structure context, links compounds to Tox21/ToxCast assays, trains or applies predictive toxicity models, and iteratively proposes which compounds / assays / targets to test next — not a single offline classifier without a decision loop.

---

## Industrial Significance

- Tox21 is a multi-agency U.S. federal program (EPA, NIEHS, NCATS, FDA) aimed at faster, more human-relevant toxicity testing and reduced animal use.
- AlphaFold DB provides >200 million predicted structures, collapsing wait times for structural context.
- Pharma, agrochemical, and consumer-chemical industries need agents that triage large libraries before expensive wet assays.
- Calgary’s life-sciences and health-innovation community can prototype decision agents that generalize to real screening portfolios.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load Tox21/ToxCast bioactivity tables (and optional PubChem assay links); fetch example PDB / AlphaFold structures for a target class.
2. **Represent:** Featurize compounds (RDKit fingerprints / descriptors) and optionally protein pockets / sequences.
3. **Predict:** Multi-task or selected-assay toxicity classifiers / regressors (DeepChem or sklearn baselines).
4. **Act & Iterate:** Active-learning style loop — select uncertain or high-risk compounds for “virtual wet-lab” evaluation, update the model, re-rank.
5. **Report:** Ranked risk lists with assay rationale and structural context links (PDB ID / UniProt / AlphaFold accession).

---

## Recommended Agent Architecture & Starter Code Pointers

```
Structures (PDB/AF) + Tox assays -> Featurize -> Model -> Acquisition policy -> Updated shortlist
```

**Starter frameworks (open source):**
- [RCSB PDB](https://www.rcsb.org/) — experimental structures (PDB format)
- [AlphaFold DB](https://alphafold.ebi.ac.uk/) — predicted structures (CC-BY-4.0); GCS bulk: `gs://public-datasets-deepmind-alphafold-v4`
- [EPA ToxCast / Tox21 downloads](https://www.epa.gov/comptox-tools/exploring-toxcast-data) and [CompTox downloadable data](https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data)
- BioPython, RDKit, DeepChem, ColabFold (for on-demand folding if needed)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
pip install -r requirements.txt
python agent_starter.py --help
```

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Assay prediction AUROC / AUPRC | Report on held-out Tox21-style labels |
| Calibration | Reliability of high-risk scores |
| Active learning gain | Improvement vs. random acquisition over iterations |
| Structure linkage | ≥1 demonstrated PDB/AlphaFold fetch integrated into the narrative |
| Autonomy | Closed propose → (virtual) test → update loop |
| Ethics / safety | No wet-lab instructions for synthesizing hazardous agents; stay on public screening data |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
EOF

cat << 'EOF' > "$ROOT/$CASE5/data/README.md"
# Data Guide — Protein-Structure-to-Toxicity Screening Agent (Stream 5)

---

## 1. EPA Tox21 / ToxCast (bioactivity)

- **ToxCast exploring page:** https://www.epa.gov/comptox-tools/exploring-toxcast-data  
- **Downloadable computational toxicology data:** https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data  
- **Tox21 program:** https://tox21.gov/data-and-tools/  
- **What:** High-throughput screening bioactivity for thousands of chemicals across many assays; `invitrodb` MySQL + `tcpl` R package for advanced users; flat-file releases also available.
- **Formats:** CSV / TSV flat files; MySQL dumps; API access via EPA CTX Bioactivity APIs
- **License:** EPA open data (free for commercial and non-commercial use per EPA open-data statements)

```bash
mkdir -p raw/toxcast
# Download the latest recommended ToxCast / Tox21 flat files from the EPA pages above.
# Prefer current invitrodb-linked releases for new work; legacy zips remain available.
```

**PubChem:** Tox21 assay records are also browsable via PubChem BioAssay for compound-centric pulls.

---

## 2. RCSB Protein Data Bank (experimental structures)

- **Portal:** https://www.rcsb.org/  
- **Format:** PDB / mmCIF  
- **REST example:**

```bash
mkdir -p raw/pdb
# Download hemoglobin structure 1A3N as an example
curl -L -o raw/pdb/1A3N.pdb https://files.rcsb.org/download/1A3N.pdb
```

Python:

```python
from Bio.PDB import PDBList
pdbl = PDBList()
pdbl.retrieve_pdb_file("1A3N", pdir="raw/pdb", file_format="pdb")
```

---

## 3. AlphaFold Protein Structure Database

- **UI:** https://alphafold.ebi.ac.uk/  
- **Bulk:** Google Cloud `gs://public-datasets-deepmind-alphafold-v4` (CC-BY-4.0)  
- **GitHub access notes:** https://github.com/google-deepmind/alphafold/tree/main/afdb  
- **Formats:** PDB / mmCIF predicted coordinates + confidence metrics (pLDDT, PAE)
- **Hackathon tip:** Download **individual** predictions for a few UniProt accessions — do not mirror hundreds of millions of structures.

Example (website download for a single prediction) or GCS for scripted pulls when cloud tooling is available.

---

## 4. Minimal starter CSV schema (compound–assay)

If EPA flat files are heavy for day-one setup, begin with a compact derived table:

| column | description |
|---|---|
| `compound_id` | Local or DSSTox / CAS identifier |
| `smiles` | Chemical structure |
| `assay_id` | Tox21/ToxCast assay identifier |
| `activity` | 1 active / 0 inactive (or continuous AC50) |

The starter agent can synthesize a toy table for pipeline testing, then you swap in real Tox21 labels.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── toxcast/
    ├── pdb/
    ├── alphafold/
    └── toy_tox21.csv
```

### Ethics note

Use public screening datasets only. Do not attempt to generate instructions for producing controlled or highly hazardous substances. Focus on ranking / triage methodology.
EOF

cat << 'EOF' > "$ROOT/$CASE5/requirements.txt"
# Stream 5 — Life Sciences & Bio-Engineering
# Requires Python 3.10+
numpy>=1.24
pandas>=2.0
scipy>=1.10
matplotlib>=3.7
scikit-learn>=1.3
requests>=2.31
# Optional next steps (can be painful on Windows): biopython, rdkit, deepchem, torch
EOF

cat << 'EOF' > "$ROOT/$CASE5/agent_starter.py"
#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 5 Starter Agent
Case: Autonomous Protein-Structure-to-Toxicity Screening Agent
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def synthesize_tox_table(path: Path, n: int = 400) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    # Toy fingerprints: 32 random bits as stand-in for Morgan FP
    fps = rng.integers(0, 2, size=(n, 32))
    # Latent toxicity rule: first 5 bits correlated with label
    logits = fps[:, :5].sum(axis=1) + rng.normal(0, 0.5, size=n)
    y = (logits > np.median(logits)).astype(int)
    df = pd.DataFrame(fps, columns=[f"fp_{i}" for i in range(32)])
    df.insert(0, "compound_id", [f"CMPD_{i:04d}" for i in range(n)])
    df["smiles"] = ["CCO"] * n  # placeholder
    df["assay_id"] = "TOY_NR_ASSAY"
    df["activity"] = y
    df.to_csv(path, index=False)
    print(f"[info] Wrote toy Tox21-like table to {path}")
    return df


def perceive(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return synthesize_tox_table(path)


def fetch_pdb_header(pdb_id: str = "1A3N") -> str:
    """Lightweight structure-context fetch (PDB header via RCSB)."""
    url = f"https://files.rcsb.org/header/{pdb_id}.pdb"
    try:
        r = requests.get(url, timeout=20)
        if r.ok:
            lines = r.text.splitlines()[:5]
            return " | ".join(lines)
    except requests.RequestException as exc:
        return f"PDB fetch failed: {exc}"
    return "PDB fetch failed"


def featurize(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    fp_cols = [c for c in df.columns if c.startswith("fp_")]
    if not fp_cols:
        raise ValueError("Expected fp_* columns (toy fingerprints) or extend with RDKit.")
    X = df[fp_cols].to_numpy()
    y = df["activity"].to_numpy()
    ids = df["compound_id"].astype(str).tolist()
    return X, y, ids


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(Xtr, ytr)
    proba = model.predict_proba(Xte)[:, 1]
    auroc = float(roc_auc_score(yte, proba)) if len(np.unique(yte)) > 1 else float("nan")
    return model, {"auroc": auroc, "n_train": len(Xtr), "n_test": len(Xte)}


def act_active_learning(model, X: np.ndarray, ids: list[str], batch: int = 10) -> list[str]:
    proba = model.predict_proba(X)[:, 1]
    uncertainty = np.abs(proba - 0.5)  # lower = more uncertain
    pick = np.argsort(uncertainty)[:batch]
    return [ids[i] for i in pick]


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    print("structure_context:", fetch_pdb_header("1A3N"))
    X, y, ids = featurize(df)
    labeled = np.zeros(len(y), dtype=bool)
    # seed labels
    labeled[:40] = True
    for i in range(1, iters + 1):
        model, metrics = reason_train(X[labeled], y[labeled])
        query_ids = act_active_learning(model, X[~labeled], [ids[j] for j in range(len(ids)) if not labeled[j]])
        # Virtual wet-lab: reveal labels for queried IDs
        id_to_idx = {cid: k for k, cid in enumerate(ids)}
        for cid in query_ids:
            labeled[id_to_idx[cid]] = True
        print(f"=== iteration {i} === metrics={metrics} queried={query_ids[:5]} ... labeled={int(labeled.sum())}")
    print("TODO: replace toy fingerprints with RDKit Morgan FPs on real Tox21 SMILES.")
    print("TODO: link AlphaFold accessions for the biological target under study.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 5 toxicity screening starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "toy_tox21.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)


if __name__ == "__main__":
    main()
EOF

# ---------------------------------------------------------------------------
# Root .gitignore (helpful for teams; optional but practical)
# ---------------------------------------------------------------------------
cat << 'EOF' > "$ROOT/.gitignore"
# Data downloads (keep READMEs only)
**/data/raw/
*.h5
*.hdf5
*.nc
*.pdb
*.cif
*.zip

# Python
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.env

# OS / IDE
.DS_Store
Thumbs.db
.idea/
.vscode/
EOF

echo "==> Repository build complete."
echo "==> Root files:"
ls -la "$ROOT" | sed -n '1,20p'
echo "==> Stream folders:"
find "$ROOT" -type d -name 'Case 1 - *' | sort
echo "Done."
