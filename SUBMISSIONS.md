# Submissions Guide — IEEE YP Industry Hackathon

**Window:** Fri Oct 2, 2026 5:00 PM MDT → Sun Oct 4, 2026 12:00 PM MDT sharp — no exceptions.
All times are **MDT (Calgary local, UTC-6)**.

## How to submit (one issue per team)

1. Go to **Issues → New Issue → Hackathon Submission → Get started** (repo goes public at 5 PM Oct 2; the form is invisible while private).
2. Fill all 10 fields: team name, 2–5 members with `@handles`, project stream, project title, tagline (3 lines max), public repo link, About (Markdown + LaTeX `$...$`), **min 2 / max 5 screenshots** (10 MB each on GitHub Free), demo video/live-site **link** (optional but recommended — YouTube unlisted or Loom; direct upload capped at 10 MB on Free), additional info.
3. The validator bot comments within a minute (`needs-review`, or `needs-fix` / `late` as applicable).

## Editing rules

- Only the teammate who clicked Submit can edit the issue body; other teammates post updates as **comments** (the original author can copy them into the body).
- Drag-drop images/video into the body or comments at any time before lock.
- Broken submission? Ask an organizer to **delete** the issue (personal-repo owner can erase instantly), then resubmit within the window.

## Deadlines & freezing

- Cron schedules are UTC: open `55 22 2 10 *` (4:55 PM MDT buffer), close `0 18 4 10 *` (12:00 PM MDT exact).
- Cron can lag 5–30 min, so the organizer manually triggers open/close workflows at 5 PM Fri / 12 PM Sun — Actions are the safety net.
- At close the form is removed and every open `submission` issue is **locked** (`resolved`): no further edits or comments.
- Issues created after 12:00 PM MDT get `late` and will not be accepted — no exceptions. Deadline is sharp at 12:00 PM MDT.

## Judging ops (1–4 PM MDT)

- Labels: `submission → needs-review/under-review → judged → winner`, plus `needs-fix`, `late`, `duplicate`.
- Export: `python scripts/export_submissions.py nagusubra/industry-hackathon-lab --out submissions.csv`
  or `gh issue list --label submission --state all --limit 200 --json number,title,author,createdAt,url,labels`.
- Winners announced 4 PM MDT.

## Fan Favourite voting

- The **Fan Favourite ($100)** winner is decided by community votes, not judges.
- Anyone can vote by adding a 👍 (**thumbs up**) reaction to the **top post** of a submission issue.
- The submission issue with the most 👍 reactions wins. See [FAN_FAVOURITE.md](FAN_FAVOURITE.md) for how to vote and how votes are counted.

## Organizer runbook

### Late September (wake-up, keeps cron armed — GitHub disables schedules after 60 idle days)
- [ ] Push any commit or run `Open/Close Submissions` with `dry_run` to re-arm schedules.
- [ ] Create labels: `submission, needs-review, under-review, judged, winner, needs-fix, late, duplicate`.

### Oct 2 ~5:00 PM MDT (manual-first)
- [ ] `Settings → General → Change visibility → Public`.
- [ ] `Settings → Features → Issues ON`; issue creation allowed for **all users** (collaborators-only OFF).
- [ ] `Actions → Open Submissions → Run workflow`; verify incognito that the form is visible; submit + delete a test issue.

### Oct 4 ~12:00 PM MDT (manual-first)
- [ ] `Actions → Close Submissions → Run workflow`; confirm template gone and issues locked.
- [ ] Export CSV for judges; judging 1–4 PM; winners 4 PM.
