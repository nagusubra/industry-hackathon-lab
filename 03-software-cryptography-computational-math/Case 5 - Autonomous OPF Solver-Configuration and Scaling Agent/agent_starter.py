#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 3 Starter Agent
Case: Autonomous OPF Solver-Configuration and Scaling Agent

Parse MATPOWER .m cases, run DC-OPF under several solver configs,
revise the search when a config is slow or infeasible, then try a larger case.
"""

from __future__ import annotations

import argparse
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


@dataclass
class Network:
    name: str
    base_mva: float
    bus_id: np.ndarray  # original bus numbers
    pd: np.ndarray  # MW
    pg_min: np.ndarray
    pg_max: np.ndarray
    gen_bus: np.ndarray  # indices into bus array
    cost_lin: np.ndarray  # $/MWh
    f_idx: np.ndarray
    t_idx: np.ndarray
    x_pu: np.ndarray
    rate_mw: np.ndarray
    status_br: np.ndarray
    status_gen: np.ndarray


@dataclass
class OpfConfig:
    method: str  # highs | highs-ds | highs-ipm
    line_limit_scale: float
    name: str


def _synthesize_case6(path: Path) -> None:
    """Write a tiny MATPOWER-like 6-bus case (not EPIGRIDS)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = """function mpc = demo_case6
mpc.version = '2';
mpc.baseMVA = 100;
mpc.bus = [
1 3 0   0  0 0 1 1 0 230 1 1.1 0.9;
2 2 0   0  0 0 1 1 0 230 1 1.1 0.9;
3 2 0   0  0 0 1 1 0 230 1 1.1 0.9;
4 1 70  20 0 0 1 1 0 230 1 1.1 0.9;
5 1 90  30 0 0 1 1 0 230 1 1.1 0.9;
6 1 80  25 0 0 1 1 0 230 1 1.1 0.9;
];
mpc.gen = [
1 0 0 30 -30 1 100 1 150 10 0 0 0 0 0 0 0 0 0 0 0;
2 0 0 30 -30 1 100 1 100 10 0 0 0 0 0 0 0 0 0 0 0;
3 0 0 30 -30 1 100 1 80  10 0 0 0 0 0 0 0 0 0 0 0;
];
mpc.branch = [
1 2 0.02 0.06 0.03 100 100 100 0 0 1 -360 360;
1 4 0.03 0.08 0.02 80  80  80  0 0 1 -360 360;
1 5 0.04 0.09 0.02 80  80  80  0 0 1 -360 360;
2 3 0.02 0.07 0.03 70  70  70  0 0 1 -360 360;
2 4 0.03 0.08 0.02 70  70  70  0 0 1 -360 360;
2 5 0.03 0.08 0.02 70  70  70  0 0 1 -360 360;
2 6 0.02 0.06 0.03 80  80  80  0 0 1 -360 360;
3 5 0.04 0.09 0.02 60  60  60  0 0 1 -360 360;
3 6 0.03 0.08 0.02 80  80  80  0 0 1 -360 360;
4 5 0.04 0.10 0.02 40  40  40  0 0 1 -360 360;
];
mpc.gencost = [
2 0 0 3 0.11 5 150;
2 0 0 3 0.085 1.2 600;
2 0 0 3 0.122 1 335;
];
"""
    path.write_text(text, encoding="utf-8")
    print(f"[warn] Synthetic demo written to {path} — not an EPIGRIDS case. Download .m files for scoring.")


def _parse_matrix(src: str, key: str) -> np.ndarray:
    """Extract mpc.<key> = [ ... ]; as a float array."""
    m = re.search(rf"mpc\.{re.escape(key)}\s*=\s*\[(.*?)\];", src, flags=re.S)
    if not m:
        raise ValueError(f"Could not find mpc.{key} in MATPOWER file")
    body = m.group(1)
    rows: list[list[float]] = []
    for line in body.splitlines():
        line = line.split("%", 1)[0].strip().rstrip(";")
        if not line:
            continue
        parts = [p for p in re.split(r"[,\s]+", line) if p]
        if parts:
            rows.append([float(p) for p in parts])
    if not rows:
        raise ValueError(f"Empty mpc.{key}")
    width = max(len(r) for r in rows)
    arr = np.zeros((len(rows), width))
    for i, r in enumerate(rows):
        arr[i, : len(r)] = r
    return arr


def parse_matpower(path: Path) -> Network:
    src = path.read_text(encoding="utf-8", errors="ignore")
    bm = re.search(r"mpc\.baseMVA\s*=\s*([0-9.eE+-]+)", src)
    base_mva = float(bm.group(1)) if bm else 100.0
    bus = _parse_matrix(src, "bus")
    gen = _parse_matrix(src, "gen")
    branch = _parse_matrix(src, "branch")
    try:
        gencost = _parse_matrix(src, "gencost")
    except ValueError:
        gencost = np.zeros((gen.shape[0], 7))
        gencost[:, 0] = 2
        gencost[:, 3] = 2
        gencost[:, 5] = 20.0  # linear $/MWh fallback

    bus_id = bus[:, 0].astype(int)
    id_to_idx = {int(b): i for i, b in enumerate(bus_id)}
    pd = bus[:, 2]
    gen_bus = np.array([id_to_idx[int(b)] for b in gen[:, 0]])
    status_gen = gen[:, 7] if gen.shape[1] > 7 else np.ones(gen.shape[0])
    pg_max = gen[:, 8]
    pg_min = gen[:, 9]
    # polynomial gencost: last n coeffs c_{n-1} ... c0; linear term is second-to-last if n>=2
    cost_lin = np.zeros(gen.shape[0])
    for i in range(min(gen.shape[0], gencost.shape[0])):
        n = int(gencost[i, 3]) if gencost.shape[1] > 3 else 2
        coeffs = gencost[i, 4 : 4 + n]
        if n >= 2:
            cost_lin[i] = coeffs[-2]  # c1 in c2 P^2 + c1 P + c0
        elif n == 1:
            cost_lin[i] = coeffs[-1]

    f_idx = np.array([id_to_idx[int(b)] for b in branch[:, 0]])
    t_idx = np.array([id_to_idx[int(b)] for b in branch[:, 1]])
    x_pu = np.clip(branch[:, 3], 1e-6, None)
    rate = branch[:, 5]
    rate = np.where(rate <= 0, 9999.0, rate)
    status_br = branch[:, 10] if branch.shape[1] > 10 else np.ones(branch.shape[0])

    return Network(
        name=path.stem,
        base_mva=base_mva,
        bus_id=bus_id,
        pd=pd,
        pg_min=pg_min,
        pg_max=pg_max,
        gen_bus=gen_bus,
        cost_lin=cost_lin,
        f_idx=f_idx,
        t_idx=t_idx,
        x_pu=x_pu,
        rate_mw=rate,
        status_br=status_br,
        status_gen=status_gen,
    )


def solve_dc_opf(net: Network, cfg: OpfConfig) -> dict[str, Any]:
    """
    Variables: [Pg (n_g), theta (n_b-1)]  (slack bus 0 angle fixed at 0).
    DC: P_i = sum_j B_ij (theta_i - theta_j); B_ij = 1/x_ij.
    """
    n_b = len(net.pd)
    n_g = len(net.pg_max)
    slack = 0
    theta_idx = [i for i in range(n_b) if i != slack]
    n_th = len(theta_idx)
    n_var = n_g + n_th

    b_bus = np.zeros((n_b, n_b))
    for k, (i, j) in enumerate(zip(net.f_idx, net.t_idx)):
        if net.status_br[k] <= 0:
            continue
        b = 1.0 / net.x_pu[k]
        b_bus[i, i] += b
        b_bus[j, j] += b
        b_bus[i, j] -= b
        b_bus[j, i] -= b

    # equality: gen injection - B theta = Pd  (MW, using P_pu * baseMVA = MW if x is pu)
    # With x in pu on baseMVA, P_mw = baseMVA * B_pu * theta_rad
    a_eq = np.zeros((n_b, n_var))
    b_eq = net.pd.copy()
    for g in range(n_g):
        if net.status_gen[g] <= 0:
            continue
        a_eq[net.gen_bus[g], g] = 1.0
    for col, bus_i in enumerate(theta_idx):
        a_eq[:, n_g + col] -= net.base_mva * b_bus[:, bus_i]

    n_br = len(net.f_idx)
    a_ub_rows: list[np.ndarray] = []
    b_ub: list[float] = []
    scale = cfg.line_limit_scale
    for k, (i, j) in enumerate(zip(net.f_idx, net.t_idx)):
        if net.status_br[k] <= 0:
            continue
        b = 1.0 / net.x_pu[k]
        flow = np.zeros(n_var)
        # P_ij = baseMVA * (theta_i - theta_j) / x
        if i != slack:
            flow[n_g + theta_idx.index(i)] += net.base_mva * b
        if j != slack:
            flow[n_g + theta_idx.index(j)] -= net.base_mva * b
        limit = net.rate_mw[k] * scale
        a_ub_rows.append(flow)
        b_ub.append(limit)
        a_ub_rows.append(-flow)
        b_ub.append(limit)

    c = np.zeros(n_var)
    c[:n_g] = net.cost_lin
    bounds = []
    for g in range(n_g):
        if net.status_gen[g] <= 0:
            bounds.append((0.0, 0.0))
        else:
            bounds.append((float(net.pg_min[g]), float(net.pg_max[g])))
    for _ in range(n_th):
        bounds.append((-np.pi / 2, np.pi / 2))

    a_ub = np.vstack(a_ub_rows) if a_ub_rows else None
    t0 = time.perf_counter()
    try:
        res = linprog(
            c,
            A_ub=a_ub,
            b_ub=np.array(b_ub) if b_ub else None,
            A_eq=a_eq,
            b_eq=b_eq,
            bounds=bounds,
            method=cfg.method,
            options={"time_limit": 10.0} if cfg.method.startswith("highs") else None,
        )
        elapsed = time.perf_counter() - t0
        feasible = bool(res.success)
        obj = float(res.fun) if feasible and res.fun is not None else float("inf")
        return {
            "config": cfg.name,
            "success": feasible,
            "objective": obj,
            "time_s": elapsed,
            "message": str(res.message),
        }
    except Exception as exc:  # noqa: BLE001
        elapsed = time.perf_counter() - t0
        return {
            "config": cfg.name,
            "success": False,
            "objective": float("inf"),
            "time_s": elapsed,
            "message": str(exc),
        }


def config_space(rng: random.Random) -> list[OpfConfig]:
    methods = ["highs", "highs-ds", "highs-ipm"]
    scales = [1.0, 1.05, 0.95]
    cfgs = [
        OpfConfig(method="highs", line_limit_scale=1.0, name="default-highs"),
    ]
    for _ in range(6):
        m = rng.choice(methods)
        s = rng.choice(scales)
        cfgs.append(
            OpfConfig(
                method=m,
                line_limit_scale=s,
                name=f"{m}|scale={s}",
            )
        )
    # unique by name
    seen: set[str] = set()
    unique: list[OpfConfig] = []
    for c in cfgs:
        if c.name not in seen:
            seen.add(c.name)
            unique.append(c)
    return unique


def evaluate(results: list[dict[str, Any]], default: dict[str, Any]) -> dict[str, Any]:
    feasible = [r for r in results if r["success"]]
    best = min(feasible, key=lambda r: (r["objective"], r["time_s"])) if feasible else default
    time_gain = default["time_s"] / max(best["time_s"], 1e-9) if best["success"] else 0.0
    cost_delta = best["objective"] - default["objective"] if default["success"] and best["success"] else float("inf")
    return {
        "best_config": best["config"],
        "best_objective": best["objective"],
        "best_time_s": best["time_s"],
        "default_objective": default["objective"],
        "default_time_s": default["time_s"],
        "time_speedup": time_gain,
        "cost_delta": cost_delta,
        "n_feasible": len(feasible),
    }


def run_on_network(net: Network, rng: random.Random, n_trials: int) -> dict[str, Any]:
    cfgs = config_space(rng)[: max(2, n_trials)]
    default = solve_dc_opf(net, cfgs[0])
    history = [default]
    strategy = "explore"
    best = default
    for i, cfg in enumerate(cfgs[1:], start=1):
        if strategy == "intensify" and best["success"]:
            cfg = OpfConfig(
                method=best["config"].split("|")[0] if "|" in best["config"] else "highs",
                line_limit_scale=1.0,
                name=f"intensify-{best['config']}-{i}",
            )
        r = solve_dc_opf(net, cfg)
        history.append(r)
        if r["success"] and (not best["success"] or r["objective"] < best["objective"] - 1e-6 or (
            abs(r["objective"] - best["objective"]) < 1e-3 and r["time_s"] < best["time_s"]
        )):
            best = r
        recent = history[-3:]
        if len(recent) == 3 and max(x["time_s"] for x in recent) < 0.05:
            strategy = "intensify"
        elif not r["success"]:
            strategy = "explore"
        print(f"  trial {i} {r['config']}: success={r['success']} obj={r['objective']:.2f} t={r['time_s']:.4f}s")
    metrics = evaluate(history, default)
    metrics["network"] = net.name
    metrics["n_bus"] = int(len(net.pd))
    metrics["strategy"] = strategy
    return metrics


def perceive_cases(raw_dir: Path) -> list[Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(raw_dir.glob("*.m"))
    if files:
        return files
    demo = raw_dir / "demo_case6.m"
    _synthesize_case6(demo)
    return [demo]


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 5 OPF solver-config search starter agent")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "epigrids",
        help="Directory of MATPOWER .m cases",
    )
    parser.add_argument("--trials", type=int, default=5, help="Configs to try per network")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    paths = perceive_cases(args.raw_dir)
    # Prefer smaller files first so the loop scales up
    paths = sorted(paths, key=lambda p: p.stat().st_size)
    print("cases:", [p.name for p in paths])

    prev: dict[str, Any] | None = None
    for path in paths[:3]:
        net = parse_matpower(path)
        print(f"=== network {net.name} ({len(net.pd)} buses) ===")
        metrics = run_on_network(net, rng, n_trials=args.trials)
        print("metrics:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in metrics.items()})
        if prev and metrics["best_time_s"] > 5 * max(prev["best_time_s"], 1e-6):
            print("[revise] runtime jumped with size — next search should prefer faster solvers / DC-only")
        prev = metrics
    print("TODO: AC-OPF via pandapower; EPIGRIDS Texas 7336-bus; warm-start across load snapshots.")


if __name__ == "__main__":
    main()
