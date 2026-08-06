#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 2 Starter Agent
Case: Autonomous Bridge Structural-Health Monitoring Agent

Minimal damage classifier on Z24-style multi-sensor vibration + iterative alert threshold.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.fft import rfft
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


N_SCENARIOS = 17
N_SETUPS = 9
N_SEGMENTS = 10
N_SENSORS = 27
N_SAMPLES = 6000
FS_HZ = 100.0


def find_z24_arrays(data_dir: Path) -> tuple[Path | None, Path | None]:
    """Locate inputs.npy and labels.npy under common Z24 download layouts."""
    candidates = [
        data_dir,
        data_dir / "Data_Z24_processed",
    ]
    for base in candidates:
        inputs = base / "inputs.npy"
        labels = base / "labels.npy"
        if inputs.exists() and labels.exists():
            return inputs, labels
    return None, None


def synthesize_z24_like(
    inputs_path: Path,
    labels_path: Path,
    n_records: int = 90,
    n_sensors: int = N_SENSORS,
    n_samples: int = 2000,
    fs_hz: float = FS_HZ,
) -> tuple[Path, Path]:
    """Create synthetic multi-sensor vibration with progressive damage labels."""
    inputs_path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(24)
    t = np.arange(n_samples) / fs_hz
    inputs = np.zeros((n_records, n_sensors, n_samples), dtype=np.float32)
    labels = np.zeros(n_records, dtype=np.int64)

    for i in range(n_records):
        scenario = i % N_SCENARIOS
        labels[i] = scenario
        damage = scenario / max(N_SCENARIOS - 1, 1)
        base_freq = 2.5 + 0.15 * damage
        for s in range(n_sensors):
            phase = rng.uniform(0, 2 * np.pi)
            amp = 0.4 * (1.0 + 0.8 * damage) * (1.0 + 0.05 * rng.normal())
            signal = amp * np.sin(2 * np.pi * base_freq * t + phase)
            signal += 0.15 * damage * np.sin(2 * np.pi * (base_freq * 3.1) * t + phase)
            signal += rng.normal(0, 0.02 + 0.04 * damage, size=n_samples)
            inputs[i, s, :] = signal.astype(np.float32)

    np.save(inputs_path, inputs)
    np.save(labels_path, labels)
    print(f"[info] Wrote synthetic Z24-like data to {inputs_path.parent}")
    return inputs_path, labels_path


def load_z24(inputs_path: Path, labels_path: Path) -> tuple[np.ndarray, np.ndarray]:
    inputs = np.load(inputs_path)
    labels = np.load(labels_path).reshape(-1)
    if labels.shape[0] != inputs.shape[0]:
        labels = np.tile(np.arange(N_SCENARIOS), N_SETUPS * N_SEGMENTS)[: inputs.shape[0]]
    return inputs, labels


def extract_features(segment: np.ndarray, fs_hz: float = FS_HZ) -> np.ndarray:
    """Per-segment features: mean RMS per sensor + dominant FFT band energies."""
    rms = np.sqrt(np.mean(segment**2, axis=1))
    spectrum = np.abs(rfft(segment, axis=1))
    freqs = np.fft.rfftfreq(segment.shape[1], d=1.0 / fs_hz)
    bands = [(0, 5), (5, 15), (15, 40)]
    band_energy = []
    for lo, hi in bands:
        mask = (freqs >= lo) & (freqs < hi)
        band_energy.append(spectrum[:, mask].mean(axis=1))
    stacked = np.concatenate([rms, *band_energy])
    return stacked.astype(np.float32)


def perceive(inputs: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = np.stack([extract_features(inputs[i]) for i in range(inputs.shape[0])])
    y = (labels > 0).astype(np.int64)
    return X, y


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    proba = model.predict_proba(Xte)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(yte, pred)),
        "f1": float(f1_score(yte, pred, zero_division=0)),
        "precision": float(precision_score(yte, pred, zero_division=0)),
        "recall": float(recall_score(yte, pred, zero_division=0)),
        "mean_damage_prob": float(np.mean(proba)),
    }
    return model, metrics, proba, yte


def act(damage_probs: np.ndarray, alert_threshold: float) -> dict:
    """Policy: flag segments above damage probability for inspection."""
    alerts = damage_probs >= alert_threshold
    priority = np.argsort(-damage_probs)
    return {
        "threshold": alert_threshold,
        "alert_rate": float(np.mean(alerts)),
        "n_alerts": int(np.sum(alerts)),
        "top_inspection_indices": priority[:5].tolist(),
    }


def evaluate(decision: dict, y_true: np.ndarray, damage_probs: np.ndarray) -> dict:
    """Score alert policy against held-out labels."""
    alerts = damage_probs >= decision["threshold"]
    tp = int(np.sum(alerts & (y_true == 1)))
    fp = int(np.sum(alerts & (y_true == 0)))
    fn = int(np.sum((~alerts) & (y_true == 1)))
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return {
        "policy_precision": float(precision),
        "policy_recall": float(recall),
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def run_loop(inputs: np.ndarray, labels: np.ndarray, iters: int = 3) -> None:
    X, y = perceive(inputs, labels)
    model, metrics, proba, y_hold = reason_train(X, y)
    print("baseline_metrics:", metrics)
    threshold = 0.5
    for i in range(1, iters + 1):
        decision = act(proba, threshold)
        scores = evaluate(decision, y_hold, proba)
        print(f"=== iteration {i} ===", decision, scores)
        if decision["alert_rate"] < 0.10:
            threshold = max(0.2, threshold - 0.05)
        elif decision["alert_rate"] > 0.60:
            threshold = min(0.95, threshold + 0.05)
        print(f"  next_threshold={threshold:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 2 Bridge SHM starter agent")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "z24",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    inputs_path, labels_path = find_z24_arrays(args.data_dir)
    if inputs_path is None or labels_path is None:
        inputs_path = args.data_dir / "inputs.npy"
        labels_path = args.data_dir / "labels.npy"
        synthesize_z24_like(inputs_path, labels_path)

    inputs, labels = load_z24(inputs_path, labels_path)
    run_loop(inputs, labels, iters=args.iters)
    print("TODO: replace synthetic/local arrays with duan908/Z24-dataset-processed from Hugging Face.")
    print("TODO: cite Maeck & De Roeck (2003) and Reynders et al. (2008); verify license before commercial use.")


if __name__ == "__main__":
    main()
