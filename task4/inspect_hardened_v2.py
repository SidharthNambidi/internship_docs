"""
Pulls full raw prompts (system + user messages) and model outputs for a
specific hardened-prompt configuration, so you can read exactly how the
model reasons when the injection still succeeds.

Edit CARRIER, DIRECTIVE, FORGED, COPIES, N below to target any row from
your hardened_results.csv.
"""

from payloads import build_payload
from hardened_test_v2 import build_hardened_messages, ask_model_hardened, score

# Change these to inspect a different row from your results.
# This defaults to sqli/aligned/forged=True/copies=8, which hit 10/10
# hijacked in your hardened_results.csv -- a good one to read closely.
CARRIER = "sqli"
DIRECTIVE = "aligned"
FORGED = True
COPIES = 8
N = 5  # how many runs to print (keep small -- this is for reading, not scoring)

payload = build_payload(CARRIER, DIRECTIVE, FORGED, COPIES)
messages = build_hardened_messages(payload)

print("=" * 70)
print(f"CONFIG: carrier={CARRIER} directive={DIRECTIVE} forged={FORGED} copies={COPIES}")
print("=" * 70)

print("\n----- SYSTEM MESSAGE -----")
print(messages[0]["content"])

print("\n----- USER MESSAGE (payload wrapped in tag) -----")
print(messages[1]["content"])

for seed in range(N):
    output = ask_model_hardened(payload, seed)
    hijacked, level = score(output)
    print(f"\n----- RUN seed={seed} | hijacked={hijacked} | level={level} -----")
    print(output)

print("\nDone.")
