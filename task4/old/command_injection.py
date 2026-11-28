from payloads import build_payload
from run_tests import ask_model, score

payload = build_payload("command_injection", "format", True, 1)
for seed in range(5):
    output = ask_model(payload, seed)
    print(f"--- run {seed} ---")
    print(output)
    print()
