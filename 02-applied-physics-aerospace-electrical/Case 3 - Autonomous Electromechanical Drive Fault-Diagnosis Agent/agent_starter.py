#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 2 Starter Agent
Case: Autonomous Electromechanical Drive Fault-Diagnosis Agent

Minimal dual-stream (current + vibration) fault classifier + iterative condition-aware policy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import scipy.io as sio
from scipy.fft import rfft
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

CONDITIONS = ["N15_M07_F10", "N09_M07_F10", "N15_M01_F10", "N15_M07_F04"]
FS_HZ = 64000.0
N_SAMPLES = 8000


def find_paderborn_mats(data_dir: Path) -> list[Path]:
    """Collect .mat files under data/raw/paderborn/."""
    if not data_dir.exists():
        return []
    return sorted(data_dir.rglob("*.mat"))


def synthesize_paderborn_like(data_dir: Path, n_per_condition: int = 20) -> list[Path]:
    """Create synthetic current + vibration .mat files for each operating condition."""
    data_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    paths: list[Path] = []
    fault_types = ["healthy", "inner", "outer", "cage"]

    for cond_idx, cond in enumerate(CONDITIONS):
        for i in range(n_per_condition):
            fault = fault_types[i % len(fault_types)]
            is_fault = 0 if fault == "healthy" else 1
            speed_factor = 1.0 if "N15" in cond else 0.6
            torque_factor = 0.7 if "M07" in cond else (0.1 if "M01" in cond else 0.4)

            t = np.arange(N_SAMPLES) / FS_HZ
            base_freq = 50.0 * speed_factor
            current = 2.0 * torque_factor * np.sin(2 * np.pi * base_freq * t)
            current += 0.1 * rng.normal(size=N_SAMPLES)
            if is_fault:
                bpfo = base_freq * 3.6
                current += 0.3 * np.sin(2 * np.pi * bpfo * t)

            vib_x = 0.5 * np.sin(2 * np.pi * base_freq * 2 * t) + 0.05 * rng.normal(size=N_SAMPLES)
            vib_y = 0.5 * np.sin(2 * np.pi * base_freq * 2 * t + 0.5) + 0.05 * rng.normal(size=N_SAMPLES)
            if is_fault:
                vib_x += 0.4 * np.sin(2 * np.pi * bpfo * t)
                vib_y += 0.35 * np.sin(2 * np.pi * bpfo * t + 0.3)

            bearing_id = f"K{i:03d}" if not is_fault else f"KA{i:03d}"
            out_dir = data_dir / bearing_id
            out_dir.mkdir(parents=True, exist_ok=True)
            fname = out_dir / f"{cond}_{bearing_id}_{i}.mat"
            sio.savemat(
                fname,
                {
                    "current": current.astype(np.float64),
                    "vibration": np.stack([vib_x, vib_y]).astype(np.float64),
                    "condition": cond,
                    "fault_label": is_fault,
                    "fault_type": fault,
                },
                do_compression=True,
            )
            paths.append(fname)

    print(f"[info] Wrote {len(paths)} synthetic Paderborn-like .mat files to {data_dir}")
    return paths


def load_mat_record(path: Path) -> tuple[np.ndarray, np.ndarray, int, str]:
    """Load current + vibration and fault label from a .mat file."""
    mat = sio.loadmat(path, squeeze_me=True)
    if "Y" in mat:
        raise ValueError(
            f"{path} appears to be an official Paderborn .mat (key 'Y' detected). "
            "Parse nested structs per data/README.md, or delete data/raw/paderborn/ "
            "and re-run to generate synthetic demo .mat files."
        )
    if "current" in mat and "vibration" in mat:
        current = np.asarray(mat["current"], dtype=np.float64).ravel()
        vibration = np.asarray(mat["vibration"], dtype=np.float64)
        fault = int(mat.get("fault_label", 0))
        cond = str(mat.get("condition", "unknown"))
        return current, vibration, fault, cond
    keys = [k for k in mat if not k.startswith("__")]
    raise ValueError(f"Unrecognized .mat schema in {path}; keys={keys}")


def extract_stream_features(signal: np.ndarray, fs_hz: float = FS_HZ) -> np.ndarray:
    rms = float(np.sqrt(np.mean(signal**2)))
    spec = np.abs(rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs_hz)
    bands = [(0, 200), (200, 2000), (2000, 10000)]
    energies = [float(spec[(freqs >= lo) & (freqs < hi)].mean()) for lo, hi in bands]
    return np.array([rms, *energies], dtype=np.float32)


def extract_dual_features(current: np.ndarray, vibration: np.ndarray) -> np.ndarray:
    cur_feat = extract_stream_features(current)
    vib_feat = np.concatenate([extract_stream_features(vibration[ch]) for ch in range(vibration.shape[0])])
    return np.concatenate([cur_feat, vib_feat])


def perceive(mat_paths: list[Path]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    features, labels, conditions = [], [], []
    for p in mat_paths:
        current, vibration, fault, cond = load_mat_record(p)
        features.append(extract_dual_features(current, vibration))
        labels.append(fault)
        conditions.append(cond)
    return np.stack(features), np.array(labels, dtype=np.int64), conditions


def reason_train(X: np.ndarray, y: np.ndarray, conditions: list[str]):
    idx = np.arange(len(y))
    Xtr, Xte, ytr, yte, idtr, idte = train_test_split(
        X, y, idx, test_size=0.25, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    proba = model.predict_proba(Xte)[:, 1]
    hold_conds = [conditions[i] for i in idte]
    metrics = {
        "accuracy": float(accuracy_score(yte, pred)),
        "f1": float(f1_score(yte, pred, zero_division=0)),
    }
    return model, metrics, proba, yte, hold_conds


def act(damage_probs: np.ndarray, conditions: list[str], threshold: float) -> dict:
    """Policy: flag records above fault probability; report per-condition alert rates."""
    alerts = damage_probs >= threshold
    by_cond: dict[str, float] = {}
    cond_arr = np.array(conditions)
    for cond in sorted(set(conditions)):
        mask = cond_arr == cond
        by_cond[cond] = float(np.mean(alerts[mask])) if mask.any() else 0.0
    return {
        "threshold": threshold,
        "alert_rate": float(np.mean(alerts)),
        "n_alerts": int(np.sum(alerts)),
        "alert_rate_by_condition": by_cond,
    }


def evaluate(decision: dict, y_true: np.ndarray, damage_probs: np.ndarray) -> dict:
    alerts = damage_probs >= decision["threshold"]
    tp = int(np.sum(alerts & (y_true == 1)))
    fp = int(np.sum(alerts & (y_true == 0)))
    fn = int(np.sum((~alerts) & (y_true == 1)))
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return {"policy_precision": float(precision), "policy_recall": float(recall)}


def run_loop(mat_paths: list[Path], iters: int = 3) -> None:
    X, y, conditions = perceive(mat_paths)
    _, metrics, proba, y_hold, hold_conds = reason_train(X, y, conditions)
    print("baseline_metrics:", metrics)
    threshold = 0.5
    for i in range(1, iters + 1):
        decision = act(proba, hold_conds, threshold)
        scores = evaluate(decision, y_hold, proba)
        print(f"=== iteration {i} ===", decision, scores)
        rates = list(decision["alert_rate_by_condition"].values())
        spread = max(rates) - min(rates) if rates else 0.0
        if spread > 0.25:
            threshold = min(0.9, threshold + 0.05)
        elif decision["alert_rate"] < 0.15:
            threshold = max(0.2, threshold - 0.05)
        print(f"  next_threshold={threshold:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 2 Drive fault-diagnosis starter agent")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "paderborn",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    mat_paths = find_paderborn_mats(args.data_dir)
    if not mat_paths:
        mat_paths = synthesize_paderborn_like(args.data_dir)

    run_loop(mat_paths, iters=args.iters)
    print("TODO: replace synthetic/local .mat files with Paderborn KAt Bearing Data Center downloads.")
    print("TODO: cite Lessmeier et al. (2016); license CC BY-NC 4.0 — non-commercial use only.")


if __name__ == "__main__":
    main()
