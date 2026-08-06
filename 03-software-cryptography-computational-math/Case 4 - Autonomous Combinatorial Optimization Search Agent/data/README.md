# Data Guide — Combinatorial Optimization Search Agent (Stream 3)

---

## 1. Download FrontierCO

- **Dataset:** https://huggingface.co/datasets/CO-Bench/FrontierCO  
- **Code:** https://github.com/sunnweiwei/FrontierCO

```bash
pip install huggingface_hub
hf download CO-Bench/FrontierCO --repo-type dataset --local-dir data/raw/frontierco
```

---

## 2. Start with One Problem Folder

**Day-one recommendation:** Pick a single problem family — e.g. `TSP/easy_test_instances/` — and do **not** load all hard sets on day one.

Other families available: CFLP, CPMP, CVRP, FJSP, MIS, MDS, STP, TSP.

```bash
# Example layout after download:
# data/raw/frontierco/TSP/easy_test_instances/
# data/raw/frontierco/CVRP/easy_test_instances/
```

---

## 3. License

- **FrontierCO:** MIT  
- Cite the FrontierCO paper and repository when reporting results.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── frontierco/
        ├── TSP/
        ├── CVRP/
        └── ...
```

The bundled `agent_starter.py` runs on **synthetic TSP/CVRP toy instances** — no download required for the starter demo.
