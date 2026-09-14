"""Export hackathon submission issues to CSV for judges.

Free-plan safe: uses unauthenticated or token-authenticated REST API
(5,000 req/hr authenticated; 30-80 teams need ~2-5 requests via pagination).

Usage:
    python scripts/export_submissions.py nagusubra/industry-hackathon-lab
    python scripts/export_submissions.py nagusubra/industry-hackathon-lab --token $GH_TOKEN --out submissions.csv
    gh issue list --label submission --state all --limit 200 --json number,title,author,createdAt,url,labels  # CLI alternative
"""

import argparse
import csv
import sys
import urllib.request
import json


def fetch_issues(repo, token=None):
    issues = []
    url = f"https://api.github.com/repos/{repo}/issues?state=all&labels=submission&per_page=100"
    while url:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as resp:
            batch = json.loads(resp.read().decode("utf-8"))
            issues.extend([i for i in batch if "pull_request" not in i])
            # paginate via Link header
            link = resp.headers.get("Link", "")
            nxt = None
            for part in link.split(","):
                if 'rel="next"' in part:
                    nxt = part[part.index("<") + 1 : part.index(">")]
            url = nxt
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="owner/repo, e.g. nagusubra/industry-hackathon-lab")
    ap.add_argument("--token", default=None)
    ap.add_argument("--out", default="submissions.csv")
    args = ap.parse_args()

    try:
        issues = fetch_issues(args.repo, args.token)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR fetching issues: {e}", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["number", "title", "author", "created_at", "state", "labels", "url"])
        for i in issues:
            w.writerow(
                [
                    i["number"],
                    i["title"],
                    i["user"]["login"],
                    i["created_at"],
                    i["state"],
                    ";".join(lb["name"] for lb in i["labels"]),
                    i["html_url"],
                ]
            )
    print(f"Wrote {len(issues)} submissions to {args.out}")


if __name__ == "__main__":
    main()
