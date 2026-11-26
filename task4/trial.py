# inspect_one.py
from payloads import build_payload
from run_tests import ask_model, score

# the winning config from your results
DIRECTIVE = "format"
FORGED = True
COPIES = 1
N = 10

payload = build_payload(DIRECTIVE, FORGED, COPIES)

print("===== PAYLOAD SENT =====")
print(payload)
print("=========================\n")

for seed in range(N):
    output = ask_model(payload, seed)
    hijacked, level = score(output)
    print(f"--- run {seed+1}/{N} | level={level} | hijacked={hijacked} ---")
    print(output)
    print()
