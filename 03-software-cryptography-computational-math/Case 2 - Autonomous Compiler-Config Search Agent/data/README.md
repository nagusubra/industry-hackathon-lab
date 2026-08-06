# Data Guide — Compiler-Config Search Agent (Stream 3)

---

## 1. Create a Kaggle Account & Download the Competition Data

- **Competition:** https://www.kaggle.com/competitions/predict-ai-model-runtime  
- **Alternative source:** https://github.com/google-research-datasets/tpu_graphs (Apache 2.0)

### Kaggle API credentials

1. Create a free account at https://www.kaggle.com/ and accept the competition rules.
2. Open **Account → API → Create New Token** — this downloads `kaggle.json`.
3. Place the token at `~/.kaggle/kaggle.json` (Linux/macOS) or `%USERPROFILE%\.kaggle\kaggle.json` (Windows).
4. Install the CLI and download:

```bash
pip install kaggle
kaggle competitions download -c predict-ai-model-runtime -p data/raw/tpugraphs
```

**Day-one recommendation:** Start with the **`tile:xla` subset only** — do not pull every collection on day one.

### GitHub alternative (`tile:xla` only)

```bash
git clone https://github.com/google-research-datasets/tpu_graphs.git data/raw/tpugraphs_repo
```

Follow the [repo README](https://github.com/google-research-datasets/tpu_graphs) to fetch **only** the `tile:xla` collection into `data/raw/tpugraphs/`.

---

## 2. Unzip into `data/raw/tpugraphs/`

```bash
cd data/raw/tpugraphs
unzip predict-ai-model-runtime.zip   # Windows: Expand-Archive predict-ai-model-runtime.zip .
```

Expected contents include graph tensors, config vectors, and measured runtimes per (graph, config) pair. See the TpuGraphs paper for schema details.

---

## 3. License

- **TpuGraphs / Kaggle competition data:** Apache 2.0  
- Cite: Phothilimthana et al., *TpuGraphs: A Performance Prediction Dataset on TPUs*, NeurIPS 2023.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── tpugraphs/          # unzipped Kaggle or tile:xla subset
    └── tpugraphs_repo/     # optional GitHub clone (fetch scripts only)
```

The bundled `agent_starter.py` runs on **synthetic small graphs** with a config→runtime oracle — no download required for the starter demo.
