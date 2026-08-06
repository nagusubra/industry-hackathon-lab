# Data Guide — Bridge Structural-Health Monitoring Agent (Stream 2)

---

## Primary Dataset: KU Leuven Z24 Bridge (Processed)

- **Hugging Face:** https://huggingface.co/datasets/duan908/Z24-dataset-processed  
- **Original campaign:** Z24 highway bridge, Switzerland — progressive damage through controlled demolition (1998)  
- **Format:** NumPy arrays — `inputs.npy` (1530, 27, 6000), `labels.npy`  
- **Structure:** 17 scenarios × 9 sensor setups × 10 segments; 27 accelerometers per segment; 6000 samples per channel  
- **Size:** ~992 MB total

### Damage Scenarios (summary)

The Z24 campaign introduces progressive damage stages (anchor loosening, concrete saw cuts, post-tensioning changes) culminating in demolition.

**Label convention:** scenario `0` = undamaged; scenarios `1`–`16` = progressive damage stages. The starter agent uses binary labels: `damaged = (label > 0)`.

### License & Citation (Important)

**No formal open license** is stated on the Hugging Face card beyond “cite KU Leuven / original papers.” Treat as **research-use only**; verify terms before any commercial deployment.

**Cite:**
- Maeck, J., & De Roeck, G. (2003). *Damage assessment of civil engineering structures by vibration monitoring.* Proceedings of the 5th International Conference on Structural Dynamics.
- Reynders, E., et al. (2008). *Fully automated (operational modal analysis) of civil engineering structures.* Mechanical Systems and Signal Processing.

---

## Download Steps

1. Install the Hugging Face Hub client:

```bash
pip install huggingface_hub
```

2. Download the processed dataset into `data/raw/z24/`:

```bash
hf download duan908/Z24-dataset-processed --repo-type dataset --local-dir data/raw/z24
```

3. Verify the download — confirm `inputs.npy` and `labels.npy` exist under `data/raw/z24/` (they may also appear in `data/raw/z24/Data_Z24_processed/` after download).

**Do not commit `data/raw/`** (~1 GB). The repository root `.gitignore` already excludes it.

### Loading Example

```python
import numpy as np
from pathlib import Path

root = Path("data/raw/z24")
for sub in [root / "Data_Z24_processed", root]:
    inputs = sub / "inputs.npy"
    labels = sub / "labels.npy"
    if inputs.exists() and labels.exists():
        X = np.load(inputs)   # (1530, 27, 6000)
        y = np.load(labels)   # scenario labels
        print(X.shape, y.shape)
        break
```

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── z24/
        ├── inputs.npy
        └── labels.npy
```
