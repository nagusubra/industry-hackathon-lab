# Data Guide — OPF Solver-Configuration Agent (Stream 3, Case 5)

Synthetic grids contain **no CEII** and are free for commercial or non-commercial use (cite the papers). Do **not** commit large `.m` / `.raw` files to GitHub.

---

## 1. Flagship: ARPA-E EPIGRIDS (Texas A&M repository)

- **Catalog:** https://electricgrids.engr.tamu.edu/electric-grid-test-cases/  
- **What:** Synthetic OPF-ready networks from the ARPA-E GRID DATA / EPIGRIDS project (Snodgrass / UW–Madison; hosted by Texas A&M).
- **Formats:** MATPOWER (`*.m`) is the one this starter parses. PowerWorld / PSS/E / PSLF are also posted.
- **Access:** Open the case page → **Dataset Download** (Google Drive folder). No CEII form required. Downloads are free; the site asks for a courtesy citation.

| Size (day-one → stretch) | Case page |
|---|---|
| New England ~250 bus | Linked from the catalog as **EPIGRIDS New England** |
| Wisconsin ~1,664 bus | Catalog → **EPIGRIDS Wisconsin** |
| Texas ~7,336 bus | https://electricgrids.engr.tamu.edu/electric-grid-test-cases/epigrids-texas/ |
| Midwest ~10,192 bus | https://electricgrids.engr.tamu.edu/electric-grid-test-cases/epigrids-midwest/ |
| Eastern Network ~78k bus | Catalog → **EPIGRIDS Eastern Network** (large RAM; optional) |

**Texas Drive folder (from the case page):** https://drive.google.com/drive/folders/1N9SjrmS1p4A-_eySAnNx3fP5CaqomLOl  
**Midwest Drive folder:** https://drive.google.com/drive/folders/1K57Au6BEjXMmLgf1bXCfFzA-ERanrCIe  

If a Drive link 404s, use the catalog page — folders move; the catalog is the source of truth.

Save MATPOWER files as:

```
data/raw/epigrids/*.m
```

---

## 2. Day-one files (no Google Drive) — same GRID DATA family / MATPOWER

Use these to debug the agent the first hour, then scale to EPIGRIDS.

**IEEE 9-bus (tiny):**

```text
https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case9.m
```

**ACTIVSg200 (200-bus Illinois synthetic, ARPA-E GRID DATA, OPF-ready):**

```text
https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case_ACTIVSg200.m
```

**Windows (PowerShell)** from the case folder:

```powershell
New-Item -ItemType Directory -Force -Path data\raw\epigrids | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case9.m" -OutFile "data\raw\epigrids\case9.m"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case_ACTIVSg200.m" -OutFile "data\raw\epigrids\case_ACTIVSg200.m"
```

**Linux / macOS:**

```bash
mkdir -p data/raw/epigrids
curl -L -o data/raw/epigrids/case9.m https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case9.m
curl -L -o data/raw/epigrids/case_ACTIVSg200.m https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case_ACTIVSg200.m
```

MATPOWER example cases are BSD-licensed (see the MATPOWER repository `LICENSE`). ACTIVSg/EPIGRIDS networks are synthetic; cite Birchfield/Overbye and Snodgrass as applicable: https://electricgrids.engr.tamu.edu/references/

---

## 3. MATPOWER `.m` fields the starter expects

```
mpc.baseMVA
mpc.bus     % bus_i, type, Pd, Qd, Gs, Bs, area, Vm, Va, baseKV, zone, Vmax, Vmin
mpc.gen     % bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin, ...
mpc.branch  % fbus, tbus, r, x, b, rateA, rateB, rateC, ratio, angle, status, ...
mpc.gencost % model, startup, shutdown, n, cN, ..., c0
```

`agent_starter.py` includes a small parser for these blocks. It does **not** execute MATLAB.

If no `.m` file is present, the starter writes **`data/raw/epigrids/demo_case6.m`** and prints `[warn]`.

---

## License & Use Terms

Texas A&M: synthetic cases are provided **free for commercial or non-commercial use**; they **do not represent the real grid**. Cite https://electricgrids.engr.tamu.edu/references/

EPIGRIDS construction: J. M. Snodgrass, *Tractable Algorithms for Constructing Electric Power Network Models*, Ph.D. thesis, University of Wisconsin–Madison, 2021.

MATPOWER data files: follow the MATPOWER BSD license when you copy `case9.m` / `case_ACTIVSg200.m`.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── epigrids/
        ├── case9.m                 # day-one
        ├── case_ACTIVSg200.m       # day-one scale-up
        └── <epigrids-texas>.m      # after Drive download
```

This lab already gitignores `**/data/raw/`.
