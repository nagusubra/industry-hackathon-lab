# Data Guide — Disruption-Aware Job-Shop Scheduling Agent (Stream 3)

---

## 1. Install Hugging Face Tooling

```bash
pip install datasets huggingface_hub
```

---

## 2. Download REALM-Bench

- **Dataset:** https://huggingface.co/datasets/GloriaGeng/REALM-Bench  
- **Code:** https://github.com/genglongling/REALM-Bench

**Option A — load via `datasets`:**

```bash
python -c "from datasets import load_dataset; ds=load_dataset('GloriaGeng/REALM-Bench'); print(ds)"
```

**Option B — download to disk:**

```bash
hf download GloriaGeng/REALM-Bench --repo-type dataset --local-dir data/raw/realm-bench
```

---

## 3. Start with J1, Then J2

| Tier | Description |
|---|---|
| **J1** | Static small JSSP — baseline scheduling without disruptions |
| **J2** | Disruptions injected (machine breakdowns, delays) — reactive replanning |
| J3/J4 | Larger instances and harder disruption patterns — stretch goals |

Begin with **J1** to validate your scheduler, then move to **J2** for disruption-aware replanning.

---

## License

- **REALM-Bench dataset:** CC-BY-4.0  
- Wraps classic JSSP benchmarks (Taillard, DMU, ABZ, etc.) — cite REALM-Bench and original instance sources.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── realm-bench/
```

The bundled `agent_starter.py` runs on a **synthetic JSSP instance** with injected disruption — no download required for the starter demo.
