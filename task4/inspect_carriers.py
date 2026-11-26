from payloads import build_payload, CARRIERS
from run_tests import ask_model, score

DIRECTIVE = "format"
FORGED = True
COPIES = 1
N = 20

for carrier_key in CARRIERS:
    print(f"\n########## CARRIER: {carrier_key} ##########")
    payload = build_payload(carrier_key, DIRECTIVE, FORGED, COPIES)
    hijacked_count = 0
    normal_count = 0
    for seed in range(N):
        output = ask_model(payload, seed)
        hijacked, level = score(output)
        says_normal = "appears normal" in output.lower() or "appears to be normal" in output.lower()
        hijacked_count += hijacked
        normal_count += says_normal
        print(f"run {seed+1}: hijacked={hijacked} says_normal={says_normal}")
    print(f"--- {carrier_key}: hijack={hijacked_count}/{N}  says_normal={normal_count}/{N} ---")
