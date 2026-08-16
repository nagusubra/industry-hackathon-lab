#!/usr/bin/env python3
"""Archive GitHub repository traffic into .metrics/data/*.csv and refresh
doc/metric/badge.svg.

GitHub only exposes the last 14 days of traffic data, so this is meant to run
on a schedule (see .github/workflows/traffic.yml). Each run fetches the full
14-day window, merges it into the persistent CSVs (newer values win) and
regenerates an all-time total-views badge.

Environment:
    GH_TOKEN            GitHub token (e.g. github.token in Actions). Optional
                        for the public repo endpoint; required for traffic.
    GITHUB_REPOSITORY   "owner/repo" (set automatically in Actions).

Stdlib only.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone

API = "https://api.github.com"
DEFAULT_REPO = "nagusubra/industry-hackathon-lab"
BRANCH = "traffic-data"

HERE = os.path.dirname(os.path.abspath(__file__))          # <root>/.github/scripts
ROOT = os.path.dirname(os.path.dirname(HERE))              # <root>
DATA_DIR = os.path.join(ROOT, ".metrics", "data")
DOC_DIR = os.path.join(ROOT, "doc", "metric")

TOKEN = os.environ.get("GH_TOKEN", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "").strip() or DEFAULT_REPO

VIEWS_FIELDS = ["date", "views", "uniques"]
CLONES_FIELDS = ["date", "clones", "uniques"]
REFERRERS_FIELDS = ["date", "referrer", "count", "uniques"]
PATHS_FIELDS = ["date", "path", "title", "count", "uniques"]
REPO_FIELDS = ["date", "stars", "forks", "watchers"]


def log(*args) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}]", *args, flush=True)


def api_get(path: str) -> dict | list | None:
    req = urllib.request.Request(API + path, method="GET")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "repo-traffic-archiver")
    req.add_header("X-GitHub-Api-Version", "2026-03-10")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"[warn] GET {path} -> HTTP {e.code} ({e.reason})")
        return None
    except urllib.error.URLError as e:
        log(f"[warn] GET {path} -> {e.reason}")
        return None


def merge_into(path: str, fields: list[str], keys: list[str], new_rows: list[dict]) -> None:
    data: dict[tuple, dict] = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row and all(row.get(k) not in (None, "") for k in keys):
                    data[tuple(row[k] for k in keys)] = row
    for row in new_rows:
        data[tuple(row[k] for k in keys)] = {k: str(row.get(k, "")) for k in fields}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for k in sorted(data):
            writer.writerow(data[k])
    log(f"wrote {path} ({len(data)} rows)")


def read_all(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r]


def archive_views() -> None:
    data = api_get(f"/repos/{REPO}/traffic/views?per=day") or {}
    rows = [
        {"date": d["timestamp"][:10], "views": d["count"], "uniques": d["uniques"]}
        for d in data.get("views", [])
    ]
    merge_into(os.path.join(DATA_DIR, "views.csv"), VIEWS_FIELDS, ["date"], rows)


def archive_clones() -> None:
    data = api_get(f"/repos/{REPO}/traffic/clones?per=day") or {}
    rows = [
        {"date": d["timestamp"][:10], "clones": d["count"], "uniques": d["uniques"]}
        for d in data.get("clones", [])
    ]
    merge_into(os.path.join(DATA_DIR, "clones.csv"), CLONES_FIELDS, ["date"], rows)


def archive_referrers() -> None:
    today = date.today().isoformat()
    data = api_get(f"/repos/{REPO}/traffic/popular/referrers") or []
    rows = [
        {"date": today, "referrer": r.get("referrer", ""), "count": r.get("count", 0), "uniques": r.get("uniques", 0)}
        for r in data
    ]
    merge_into(os.path.join(DATA_DIR, "referrers.csv"), REFERRERS_FIELDS, ["date", "referrer"], rows)


def archive_paths() -> None:
    today = date.today().isoformat()
    data = api_get(f"/repos/{REPO}/traffic/popular/paths") or []
    rows = [
        {
            "date": today,
            "path": p.get("path", ""),
            "title": p.get("title", ""),
            "count": p.get("count", 0),
            "uniques": p.get("uniques", 0),
        }
        for p in data
    ]
    merge_into(os.path.join(DATA_DIR, "paths.csv"), PATHS_FIELDS, ["date", "path"], rows)


def archive_repo() -> None:
    data = api_get(f"/repos/{REPO}")
    if not data:
        return
    rows = [
        {
            "date": date.today().isoformat(),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "watchers": data.get("watchers_count", 0),
        }
    ]
    merge_into(os.path.join(DATA_DIR, "repo.csv"), REPO_FIELDS, ["date"], rows)


def format_int(n) -> str:
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return "0"


def render_badge(label: str, value: str, color: str = "#2d9cdb") -> None:
    # shields.io-style badge, left label on grey, right value in color.
    font = 11
    lw = int(len(label) * 7.1 + 14)
    rw = int(len(value) * 7.6 + 14)
    W, H = lw + rw, 20
    lcx, rcx = lw // 2, lw + rw // 2
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{lw}" height="{H}" fill="#555"/>
    <rect x="{lw}" width="{rw}" height="{H}" fill="{color}"/>
    <rect width="{W}" height="{H}" fill="url(#s)"/>
  </g>
  <defs><linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-opacity=".08"/></linearGradient></defs>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="{font}">
    <text x="{lcx}" y="14">{label}</text>
    <text x="{rcx}" y="14" font-weight="bold">{value}</text>
  </g>
</svg>
"""
    os.makedirs(DOC_DIR, exist_ok=True)
    path = os.path.join(DOC_DIR, "badge.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    log(f"wrote {path}")


def refresh_badge() -> None:
    total = sum(int(r.get("views", 0) or 0) for r in read_all(os.path.join(DATA_DIR, "views.csv")))
    render_badge("total views", format_int(total), "#2d9cdb")


def main() -> int:
    if not os.environ.get("CI"):
        log(f"local run | repo={REPO} | token={'present' if TOKEN else 'MISSING (traffic endpoints will be skipped)'}")
    log(f"archiving traffic for {REPO}")
    archive_views()
    archive_clones()
    archive_referrers()
    archive_paths()
    archive_repo()
    refresh_badge()
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
