"""
Computes ASR (Attack Success Rate) summaries from a results CSV with
columns: carrier, directive, forged, copies, normal, uncertain,
flagged_malicious, hijacked.

Usage:
    python3 compute_asr.py results.csv

If duplicate rows exist for the same (carrier, directive, forged, copies)
combination -- e.g. from merging two separate runs -- their counts are
automatically summed together rather than treated as separate entries.

Prints:
  1. Per-row rates (one line per unique config)
  2. Aggregated rates by directive
  3. Aggregated rates by forged (delimiter escaping on/off)
  4. Aggregated rates by copies (duplication level)
  5. Aggregated rates by carrier
  6. The single best config by hijack rate, and by normal rate
  7. Overall average across everything
"""

import csv
import sys
from collections import defaultdict


def load_and_merge(path):
    """Reads the CSV and sums counts for duplicate (carrier, directive,
    forged, copies) rows instead of treating them as separate entries."""
    merged = defaultdict(lambda: {"normal": 0, "uncertain": 0,
                                   "flagged_malicious": 0, "hijacked": 0})
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["carrier"], row["directive"], row["forged"], row["copies"])
            for field in ["normal", "uncertain", "flagged_malicious", "hijacked"]:
                merged[key][field] += int(row[field])
    return merged


def n_of(counts):
    return counts["normal"] + counts["uncertain"] + counts["flagged_malicious"]


def rates(counts):
    n = n_of(counts)
    if n == 0:
        return 0, 0
    return counts["normal"] / n * 100, counts["hijacked"] / n * 100


def aggregate_by(merged, index):
    """index: 0=carrier, 1=directive, 2=forged, 3=copies"""
    groups = defaultdict(lambda: {"normal": 0, "uncertain": 0,
                                   "flagged_malicious": 0, "hijacked": 0})
    for key, counts in merged.items():
        group_key = key[index]
        for field in counts:
            groups[group_key][field] += counts[field]
    return groups


def print_group(title, groups, order=None):
    print(f"\n--- {title} ---")
    keys = order if order else sorted(groups.keys())
    for k in keys:
        if k not in groups:
            continue
        n = n_of(groups[k])
        normal_rate, hijack_rate = rates(groups[k])
        print(f"{str(k):20s} n={n:5d}  normal={normal_rate:5.1f}%  hijack={hijack_rate:5.1f}%")


def main(path):
    merged = load_and_merge(path)

    print("=" * 70)
    print(f"ASR SUMMARY: {path}")
    print(f"Unique configurations: {len(merged)}")
    print("=" * 70)

    print("\n--- Per-config rates ---")
    for key in sorted(merged.keys()):
        carrier, directive, forged, copies = key
        n = n_of(merged[key])
        normal_rate, hijack_rate = rates(merged[key])
        print(f"{carrier:18s} {directive:8s} forged={forged:5s} copies={copies:2s}  "
              f"n={n:3d}  normal={normal_rate:5.1f}%  hijack={hijack_rate:5.1f}%")

    print_group("By carrier", aggregate_by(merged, 0))
    print_group("By directive", aggregate_by(merged, 1), order=["direct", "aligned", "format"])
    print_group("By forged (delimiter escaping)", aggregate_by(merged, 2), order=["False", "True"])
    print_group("By copies (duplication)", aggregate_by(merged, 3), order=["1", "2", "4", "8"])

    # Best configs
    best_hijack_key = max(merged, key=lambda k: rates(merged[k])[1])
    best_normal_key = max(merged, key=lambda k: rates(merged[k])[0])
    print("\n--- Best single configs ---")
    print(f"Highest hijack rate : {best_hijack_key}  -> "
          f"normal={rates(merged[best_hijack_key])[0]:.1f}%  "
          f"hijack={rates(merged[best_hijack_key])[1]:.1f}%")
    print(f"Highest normal rate : {best_normal_key}  -> "
          f"normal={rates(merged[best_normal_key])[0]:.1f}%  "
          f"hijack={rates(merged[best_normal_key])[1]:.1f}%")

    # Overall average
    total = {"normal": 0, "uncertain": 0, "flagged_malicious": 0, "hijacked": 0}
    for counts in merged.values():
        for field in total:
            total[field] += counts[field]
    n = n_of(total)
    normal_rate, hijack_rate = rates(total)
    print("\n--- Overall average across all configs ---")
    print(f"n={n}  normal={normal_rate:.1f}%  hijack={hijack_rate:.1f}%")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "results.csv"
    main(path)
