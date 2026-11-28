import csv
from run_tests import run_experiment

CARRIER = "sqli"
DIRECTIVE = "format"
COPIES = 1
N = 20  # trials per condition

if __name__ == "__main__":
    with open("forged_comparison_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["carrier", "directive", "forged", "copies",
                          "normal", "uncertain", "flagged_malicious", "hijacked"])

        for forged in [False, True]:
            print(f"\n=== forged: {forged} ===")
            res = run_experiment(CARRIER, DIRECTIVE, forged, COPIES, n=N)
            row = [CARRIER, DIRECTIVE, forged, COPIES,
                   res["normal"], res["uncertain"], res["flagged_malicious"], res["hijacked"]]
            writer.writerow(row)
            f.flush()
            print(row)

    print("\nDone. Results saved to forged_comparison_results.csv")
