from payloads import build_payload, CARRIERS
from run_tests import ask_model, score          # undefended analyzer

SEP = "=" * 70


def pause():
    input("\n[press Enter to continue]\n")


def section(title, explanation):
    print("\n" + SEP)
    print(title)
    print(SEP)
    print(explanation)


def run_and_show(label, ask_fn, payload, seed=0):
    print(f"\n--- {label} ---")
    output = ask_fn(payload, seed)
    hijacked, level = score(output)
    print(output)
    print(f"\n[scored: level={level}, hijacked={hijacked}]")
    return output, hijacked, level


# ---------------------------------------------------------------
section(
    "1. BASELINE: Undefended analyzer, no injection",
    "The analyzer correctly identifies a SQL injection attempt with no\n"
    "attack present. This is the system working as intended."
)
baseline_payload = build_payload("sqli", "format", use_forged_structure=False, copies=0)
run_and_show("Plain SQLi payload, undefended analyzer", ask_model, baseline_payload, seed=1)
pause()

# ---------------------------------------------------------------
section(
    "2. ATTACK: Delimiter escaping is necessary",
    "Same directive, same carrier -- only difference is whether the\n"
    "injected text includes a forged 'END OF PAYLOAD' structural marker.\n"
    "Without it, the canary never appears. With it, the attack succeeds."
)
no_forge = build_payload("sqli", "format", use_forged_structure=False, copies=1)
with_forge = build_payload("sqli", "format", use_forged_structure=True, copies=1)
run_and_show("Injection WITHOUT forged structure", ask_model, no_forge, seed=2)
run_and_show("Injection WITH forged structure", ask_model, with_forge, seed=2)
pause()

# ---------------------------------------------------------------
section(
    "3. ATTACK: Behavioral target shift beats blunt override",
    "Three directive wordings on the same carrier, same structure.\n"
    "'format' (fake pipeline requirement) consistently outperforms\n"
    "'direct' (blunt override) and 'aligned' (fake authorization)."
)
for directive in ["direct", "aligned", "format"]:
    p = build_payload("sqli", directive, use_forged_structure=True, copies=1)
    run_and_show(f"Directive = {directive}", ask_model, p, seed=3)
pause()

# ---------------------------------------------------------------
section(
    "4. ATTACK: Instruction duplication is counterproductive",
    "Repeating the same directive across more header fields does NOT\n"
    "improve success -- hijack rate declines as copies increase."
)
for copies in [1, 8]:
    p = build_payload("sqli", "format", use_forged_structure=True, copies=copies)
    run_and_show(f"Copies = {copies}", ask_model, p, seed=4)
pause()

# ---------------------------------------------------------------
section(
    "5. ATTACK: Generalization across attack types",
    "The winning configuration (format, forged=True, copies=1) is run\n"
    "against several different carrier attack types, including a\n"
    "benign control, to confirm the technique isn't SQLi-specific."
)
for carrier in CARRIERS:
    p = build_payload(carrier, "format", use_forged_structure=True, copies=1)
    run_and_show(f"Carrier = {carrier}", ask_model, p, seed=5)
pause()

# ---------------------------------------------------------------
section(
    "SUMMARY TABLE (fill in with your final numbers)",
    "Baseline (untuned attack)     : ~50% success\n"
    "Delimiter escaping (forged)   : required -- 0% hijack without it\n"
    "Best directive (format)       : 90% hijack on primary carrier\n"
    "Duplication (1 -> 8 copies)   : hijack rate declines monotonically\n"
    "Final winning config, averaged across carriers (n=100/carrier):\n"
    "  suppression ASR = 97%, hijack ASR = 87%\n"
)
print("\nEnd of demo.")
