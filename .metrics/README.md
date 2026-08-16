# Traffic Monitoring (owner notes)

This directory is hidden from GitHub's file browser (dot-prefix). It holds the
persistent archive powering the public dashboard. **Do not link it from the README.**

## Layout

| Path | Purpose |
|---|---|
| `data/views.csv` | daily views + unique visitors |
| `data/clones.csv` | daily clones + unique cloners |
| `data/referrers.csv` | top-10 referring sites, snapshotted per run |
| `data/paths.csv` | top-10 popular paths, snapshotted per run |
| `data/repo.csv` | daily stars / forks / watchers |

The archiver is `.github/scripts/archive_traffic.py`, triggered hourly by
`.github/workflows/traffic.yml` (also on push to `main` and manually via the
workflow dispatch button). It backfills GitHub's 14-day window on the first run.

`main` is protected (PRs required), so the workflow writes the archive to the
**`traffic-data` branch**, which the dashboard and badge read from via
`raw.githubusercontent.com`.

## Public URLs

- Dashboard: `https://nagusubra.github.io/industry-hackathon-lab/doc/metric/dashboard/`
- Badge (all-time total views, auto-refreshed hourly): `https://raw.githubusercontent.com/nagusubra/industry-hackathon-lab/traffic-data/doc/metric/badge.svg`

## How to add another repo

Copy this setup into the target repo and set `GITHUB_REPOSITORY`/`REPO`
(defaults to this repo in the script). No secret needed: the workflow's
auto-generated `github.token` can read traffic for repos the owner has access to.
