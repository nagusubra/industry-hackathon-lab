#!/usr/bin/env bash
# =============================================================================
# IEEE YP Industry Hackathon Lab
# =============================================================================
# The committed Markdown, Python, and seed CSV files in this repository are
# the source of truth.
#
# This script used to generate the old five-stream / 24-case lab. It is now a
# no-op so a leftover `bash build_repo.sh` cannot overwrite the live cases.
# =============================================================================

set -euo pipefail

echo "build_repo.sh does not generate cases anymore."
echo "Edit README.md, JUDGING_RUBRIC.md, and the three stream folders directly."
echo "Current streams:"
echo "  01-energy-and-infrastructure-systems"
echo "  02-software-and-computational-math"
echo "  03-chemical-systems-and-material-science"
exit 0
