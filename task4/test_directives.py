"""
Tests normal-verdict (suppression) rate across the three target-shift
directives (direct, aligned, format), holding the other winning
conditions fixed: carrier = sqli, forged = True (delimiter escaping on),
copies = 1.

This isolates directive wording as the only variable.
"""

import csv
from run_tests import run_experiment

CARRIER = "sqli"
FORGED = True
COPIES = 1
N = 20  # trials per directive

if __name__ == "__main__":
    with open("directive_comparison_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["carrier", "directive", "forged", "copies",
                          "normal", "uncertain", "flagged_malicious", "hijacked"])

        for directive in ["direct", "aligned", "format"]:
            print(f"\n=== directive: {directive} ===")
            res = run_experiment(CARRIER, directive, FORGED, COPIES, n=N)
            row = [CARRIER, directive, FORGED, COPIES,
                   res["normal"], res["uncertain"], res["flagged_malicious"], res["hijacked"]]
            writer.writerow(row)
            f.flush()
            print(row)

    print("\nDone. Results saved to directive_comparison_results.csv")
