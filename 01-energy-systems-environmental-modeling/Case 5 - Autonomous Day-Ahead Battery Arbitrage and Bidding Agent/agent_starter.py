#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Day-Ahead Battery Arbitrage and Bidding Agent
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Forecast next-day PJM/COMED prices, bid a feasible battery trajectory,
settle against realized prices, compare to baselines, revise.
Do not import epftoolbox (AGPL-3.0) — this script reads the Zenodo CSV only.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

PJM_URL = "https://zenodo.org/records/4624805/files/PJM.csv"
PRICE_COL = "Zonal COMED price"
DATE_COL = "Date"


@dataclass
class BatterySpec:
    power_mw: float = 10.0
    energy_mwh: float = 40.0
    eta_charge: float = 0.95
    eta_discharge: float = 0.95
    degradation_usd_per_mwh: float = 2.0
    init_soc: float = 20.0
    soc_bins: int = 21


@dataclass
class DispatchResult:
    charge_mw: np.ndarray
    discharge_mw: np.ndarray
    soc_mwh: np.ndarray
    notes: str


def _synthesize_pjm_demo(path: Path, periods: int = 24 * 28) -> None:
    """Write a labeled synthetic COMED-like series when Zenodo is unavailable."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(13)
    t = pd.date_range("2018-01-01", periods=periods, freq="h")
    hour = np.array([ts.hour for ts in t], dtype=float)
    weekday = np.array([ts.dayofweek for ts in t], dtype=float)
    load_sys = 85_000 + 8_000 * np.sin((hour - 8) * np.pi / 12) + rng.normal(0, 1200, periods)
    load_zone = 11_000 + 1_500 * np.sin((hour - 8) * np.pi / 12) + rng.normal(0, 200, periods)
    price = (
        28
        + 18 * np.sin((hour - 17) * np.pi / 8)
        + 6 * (weekday >= 5)
        + 0.0008 * (load_zone - 11_000)
        + rng.normal(0, 4, periods)
    )
    price = np.clip(price, 8, None)
    df = pd.DataFrame(
        {
            DATE_COL: t,
            PRICE_COL: price,
            "System load forecast": load_sys,
            "Zonal COMED load foecast": load_zone,
        }
    )
    df.to_csv(path, index=False)
    print(f"[warn] Synthetic demo written to {path} — not the Zenodo PJM benchmark. Download PJM.csv for scoring.")


def _download_pjm(dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        import urllib.request

        req = urllib.request.Request(
            PJM_URL,
            headers={"User-Agent": "Mozilla/5.0 (compatible; industry-hackathon-lab/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())
        df = pd.read_csv(dest, skipinitialspace=True)
        df.columns = [c.strip() for c in df.columns]
        if DATE_COL not in df.columns or PRICE_COL not in df.columns:
            print("[warn] Downloaded CSV missing expected columns:", list(df.columns))
            dest.unlink(missing_ok=True)
            return False
        df.to_csv(dest, index=False)
        print(f"[info] Downloaded Zenodo PJM.csv -> {dest} ({len(df)} rows)")
        return True
    except Exception as exc:  # noqa: BLE001 — network/IO fallback is intentional
        print(f"[warn] PJM.csv download failed ({exc})")
        if dest.exists() and dest.stat().st_size < 1000:
            dest.unlink(missing_ok=True)
        return False


def perceive(csv_path: Path) -> pd.DataFrame:
    """Load PJM.csv; download from Zenodo; else write demo_pjm.csv."""
    demo_path = csv_path.parent / "demo_pjm.csv"
    if not csv_path.exists():
        if not _download_pjm(csv_path):
            _synthesize_pjm_demo(demo_path)
            csv_path = demo_path

    df = pd.read_csv(csv_path, skipinitialspace=True)
    df.columns = [c.strip() for c in df.columns]
    colmap = {c.strip(): c for c in df.columns}
    date_col = colmap.get(DATE_COL, df.columns[0])
    price_col = colmap.get(PRICE_COL, df.select_dtypes(include="number").columns[0])
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    df = df.rename(columns={date_col: "timestamp", price_col: "price"})
    sys_col = next((c for c in df.columns if "system load" in c.lower()), None)
    zone_col = next((c for c in df.columns if "comed load" in c.lower()), None)
    if sys_col:
        df = df.rename(columns={sys_col: "system_load_da"})
    if zone_col:
        df = df.rename(columns={zone_col: "comed_load_da"})
    return df


def persistence_forecast(prices: np.ndarray, horizon: int = 24) -> np.ndarray:
    """Same-hour yesterday persistence (classic EPF baseline)."""
    if len(prices) < horizon:
        return np.full(horizon, float(np.nanmean(prices)))
    return prices[-horizon:].copy()


def dispatch_dp(prices: np.ndarray, spec: BatterySpec) -> DispatchResult:
    """Discrete-SOC DP: max revenue minus degradation over one day."""
    t_steps = len(prices)
    bins = spec.soc_bins
    soc_grid = np.linspace(0.0, spec.energy_mwh, bins)
    dt = 1.0  # hours
    max_ch = spec.power_mw * dt
    max_dis = spec.power_mw * dt

    value = np.full((t_steps + 1, bins), -1e18)
    value[t_steps, :] = 0.0
    policy = np.zeros((t_steps, bins, 2))  # charge, discharge MWh

    for t in range(t_steps - 1, -1, -1):
        p = float(prices[t])
        for i, soc in enumerate(soc_grid):
            best = -1e18
            best_u = (0.0, 0.0)
            for j, soc_next in enumerate(soc_grid):
                delta = soc_next - soc
                if delta >= 0:
                    energy_from_grid = delta / spec.eta_charge
                    if energy_from_grid - 1e-9 > max_ch:
                        continue
                    charge, discharge = energy_from_grid, 0.0
                else:
                    energy_to_grid = (-delta) * spec.eta_discharge
                    if energy_to_grid - 1e-9 > max_dis:
                        continue
                    charge, discharge = 0.0, energy_to_grid
                throughput = charge + discharge
                reward = p * (discharge - charge) - spec.degradation_usd_per_mwh * throughput
                cand = reward + value[t + 1, j]
                if cand > best:
                    best = cand
                    best_u = (charge, discharge)
            value[t, i] = best
            policy[t, i] = best_u

    init_idx = int(np.argmin(np.abs(soc_grid - spec.init_soc)))
    charge = np.zeros(t_steps)
    discharge = np.zeros(t_steps)
    soc = np.zeros(t_steps + 1)
    soc[0] = soc_grid[init_idx]
    i = init_idx
    for t in range(t_steps):
        ch, dis = policy[t, i]
        charge[t], discharge[t] = ch, dis
        soc[t + 1] = soc[t] + spec.eta_charge * ch - (dis / spec.eta_discharge if spec.eta_discharge else 0.0)
        i = int(np.argmin(np.abs(soc_grid - soc[t + 1])))
    return DispatchResult(charge, discharge, soc, notes="dp-dispatch")


def dispatch_threshold(prices: np.ndarray, spec: BatterySpec, lo: float, hi: float) -> DispatchResult:
    """Naive baseline: charge below lo, discharge above hi."""
    t_steps = len(prices)
    charge = np.zeros(t_steps)
    discharge = np.zeros(t_steps)
    soc = np.zeros(t_steps + 1)
    soc[0] = spec.init_soc
    for t, p in enumerate(prices):
        if p <= lo:
            room = spec.energy_mwh - soc[t]
            ch = min(spec.power_mw, room / spec.eta_charge)
            charge[t] = max(0.0, ch)
        elif p >= hi:
            avail = soc[t] * spec.eta_discharge
            discharge[t] = max(0.0, min(spec.power_mw, avail))
        soc[t + 1] = soc[t] + spec.eta_charge * charge[t] - (
            discharge[t] / spec.eta_discharge if spec.eta_discharge else 0.0
        )
        soc[t + 1] = float(np.clip(soc[t + 1], 0.0, spec.energy_mwh))
    return DispatchResult(charge, discharge, soc, notes=f"threshold lo={lo:.2f} hi={hi:.2f}")


def settle(realized: np.ndarray, action: DispatchResult, spec: BatterySpec) -> dict[str, float]:
    throughput = action.charge_mw + action.discharge_mw
    energy_rev = float(np.sum(realized * (action.discharge_mw - action.charge_mw)))
    deg = spec.degradation_usd_per_mwh * float(np.sum(throughput))
    cycles = float(np.sum(throughput)) / (2.0 * spec.energy_mwh)
    soc_hi = float(np.max(action.soc_mwh))
    soc_lo = float(np.min(action.soc_mwh))
    return {
        "revenue_usd": energy_rev - deg,
        "energy_revenue_usd": energy_rev,
        "degradation_usd": deg,
        "cycles": cycles,
        "soc_max_mwh": soc_hi,
        "soc_min_mwh": soc_lo,
        "soc_violation": float(soc_hi > spec.energy_mwh + 1e-6 or soc_lo < -1e-6),
    }


def evaluate(
    realized: np.ndarray,
    forecasted: np.ndarray,
    spec: BatterySpec,
    lo: float,
    hi: float,
) -> dict[str, Any]:
    bid = dispatch_dp(forecasted, spec)
    perfect = dispatch_dp(realized, spec)
    naive = dispatch_threshold(realized, spec, lo=lo, hi=hi)
    bid_m = settle(realized, bid, spec)
    pf_m = settle(realized, perfect, spec)
    nv_m = settle(realized, naive, spec)
    capture = bid_m["revenue_usd"] / pf_m["revenue_usd"] if abs(pf_m["revenue_usd"]) > 1e-6 else 0.0
    mae = float(np.mean(np.abs(forecasted - realized)))
    return {
        "bid": bid_m,
        "perfect": pf_m,
        "naive": nv_m,
        "capture_ratio": capture,
        "forecast_mae": mae,
        "lift_vs_naive_usd": bid_m["revenue_usd"] - nv_m["revenue_usd"],
    }


def run_agent_loop(df: pd.DataFrame, spec: BatterySpec, max_iters: int = 3, seed: int = 0) -> None:
    """Walk a few held-out days; revise persistence vs. mean-revert mix."""
    prices = df["price"].to_numpy(dtype=float)
    n = len(prices)
    day_len = 24
    if n < day_len * 4:
        raise ValueError("Need at least 4 days of hourly data.")
    test_start = n - day_len * 3
    mix = 1.0  # 1 = pure persistence
    rng = np.random.default_rng(seed)

    for i in range(1, max_iters + 1):
        day_idx = test_start + ((i - 1) % 3) * day_len
        hist = prices[:day_idx]
        realized = prices[day_idx : day_idx + day_len]
        persist = persistence_forecast(hist, horizon=day_len)
        climatology = np.array([float(np.mean(hist[h::24])) for h in range(day_len)])
        forecast = mix * persist + (1.0 - mix) * climatology
        lo, hi = float(np.quantile(hist, 0.30)), float(np.quantile(hist, 0.70))
        metrics = evaluate(realized, forecast, spec, lo, hi)
        print(f"=== iteration {i} (mix={mix:.2f}) ===")
        print("day_start:", df["timestamp"].iloc[day_idx])
        print("forecast_mae:", round(metrics["forecast_mae"], 3))
        print("bid_revenue_usd:", round(metrics["bid"]["revenue_usd"], 2))
        print("perfect_usd:", round(metrics["perfect"]["revenue_usd"], 2))
        print("naive_usd:", round(metrics["naive"]["revenue_usd"], 2))
        print("capture_ratio:", round(metrics["capture_ratio"], 3))
        print("lift_vs_naive_usd:", round(metrics["lift_vs_naive_usd"], 2))
        if metrics["capture_ratio"] < 0.4:
            mix = max(0.2, mix - 0.25)
            print("[revise] capture low — blending more climatology")
        else:
            mix = min(1.0, mix + 0.1)
            print("[revise] capture ok — more persistence")
        _ = rng  # reserved for stochastic bidding stretch goals
    print("TODO: replace persistence with a LASSO/LEAR-style model; add CVaR bids.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 5 PJM day-ahead battery bidding starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "epftoolbox" / "PJM.csv",
        help="Path to Zenodo PJM.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    parser.add_argument("--power-mw", type=float, default=10.0)
    parser.add_argument("--energy-mwh", type=float, default=40.0)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    spec = BatterySpec(power_mw=args.power_mw, energy_mwh=args.energy_mwh)
    df = perceive(args.csv)
    run_agent_loop(df, spec, max_iters=args.iters, seed=args.seed)


if __name__ == "__main__":
    main()
