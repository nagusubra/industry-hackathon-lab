# Data Guide — Transit Fleet Remaining Life (Case 4)

The **story** is Calgary Transit / City Fleet. The **file** is NASA C-MAPSS FD001 because municipal engine logs are not public.

FD001 train/test/RUL files are already in this folder.

---

## Bundled seed

| File | What it is |
|---|---|
| `train_FD001.txt` | 100 train engines, run to failure (space-separated, no header) |
| `test_FD001.txt` | 100 test engines, truncated before failure |
| `RUL_FD001.txt` | Remaining cycles after the last test row, one integer per test engine |
| `train_FD001_engines_1to5.csv` | Same train schema, engines 1–5 only, for a fast first plot |

Do **not** use FD002–FD004 on day one.

---

## Schema

26 columns:

| Columns | Meaning |
|---|---|
| `unit_nr` | Engine id |
| `time_cycles` | Cycle count |
| `setting_1`, `setting_2`, `setting_3` | Operating settings |
| `s_1` … `s_21` | Sensor readings |

---

## Loading example

```python
import pandas as pd

cols = ["unit_nr", "time_cycles", "setting_1", "setting_2", "setting_3"] + [f"s_{i}" for i in range(1, 22)]
train = pd.read_csv("data/train_FD001.txt", sep=r"\s+", header=None, names=cols)
rul = pd.read_csv("data/RUL_FD001.txt", sep=r"\s+", header=None, names=["RUL"])
```

---

## Source and licence

NASA Prognostics Center of Excellence — Turbofan / C-MAPSS (U.S. government work; cite NASA Ames PCoE).

Landing page: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

---

## Citation

Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. NASA Ames Prognostics Data Repository.
