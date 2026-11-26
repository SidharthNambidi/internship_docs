from payloads import build_payload, CARRIERS, CANARY
from run_tests import ask_model, score

SEP = "=" * 60


def show(title, payload, output, hijacked=None, level=None):
    print(f"\n{SEP}")
    print(title)
    print(SEP)
    print("--- PAYLOAD SENT ---")
    print(payload)
    print("\n--- MODEL OUTPUT ---")
    print(output)
    if hijacked is not None:
        print(f"\n[scored: hijacked={hijacked}, level={level}]")
    print(SEP)


# ---------- 1. Baseline: plain malicious payload, no injection ----------
baseline_payload = build_payload("sqli", "format", use_forged_structure=False, copies=0)
baseline_output = ask_model(baseline_payload, seed=1)
show("1. BASELINE (no injection, undefended analyzer)",
     baseline_payload, baseline_output)


# ---------- 2. Success: winning config on SQLi ----------
success_payload = build_payload("sqli", "format", use_forged_structure=True, copies=1)
found_success = False
for seed in range(20):
    output = ask_model(success_payload, seed)
    hijacked, level = score(output)
    says_normal = "appears normal" in output.lower() or "appears to be normal" in output.lower()
    if hijacked and says_normal:
        show(f"2. SUCCESSFUL ATTACK (seed={seed})",
             success_payload, output, hijacked, level)
        found_success = True
        break
if not found_success:
    print("\nNo full success found in 20 seeds — try more seeds or a different carrier.")


# ---------- 3. Resisted: winning config on command_injection ----------
resisted_payload = build_payload("command_injection", "format", use_forged_structure=True, copies=1)
found_resisted = False
for seed in range(20):
    output = ask_model(resisted_payload, seed)
    hijacked, level = score(output)
    says_normal = "appears normal" in output.lower() or "appears to be normal" in output.lower()
    # "resisted" = model did NOT settle on a clean normal verdict
    if not says_normal:
        show(f"3. RESISTED ATTACK (seed={seed})",
             resisted_payload, output, hijacked, level)
        found_resisted = True
        break
if not found_resisted:
    print("\nNo resisted case found in 20 seeds on command_injection — try path_traversal instead.")

print("\nDone. Screenshot each block above individually.")
