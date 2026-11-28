from payloads import build_payload, CARRIERS, DIRECTIVES

SEP = "=" * 70

carrier_list = list(CARRIERS.keys())
directive_list = list(DIRECTIVES.keys())


def choose(prompt_label, options):
    print(f"\n{prompt_label}")
    for i, opt in enumerate(options, start=1):
        print(f"  {i} = {opt}")
    while True:
        raw = input(f"Enter number (1-{len(options)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Invalid choice, try again.")


def choose_forged():
    while True:
        raw = input("\nForged structure? Enter 1 (on) or 0 (off): ").strip()
        if raw in ("0", "1"):
            return raw == "1"
        print("Invalid choice, enter 0 or 1.")


def choose_copies():
    while True:
        raw = input("\nNumber of copies (e.g. 1, 2, 4, 8): ").strip()
        if raw.isdigit() and int(raw) >= 0:
            return int(raw)
        print("Invalid choice, enter a non-negative integer.")


if __name__ == "__main__":
    print("===== Payload Generator =====")

    carrier = choose("Select carrier:", carrier_list)
    directive = choose("Select directive:", directive_list)
    forged = choose_forged()
    copies = choose_copies()

    payload = build_payload(carrier, directive, forged, copies)

    print("\n" + SEP)
    print(f"CARRIER={carrier}  DIRECTIVE={directive}  FORGED={forged}  COPIES={copies}")
    print(SEP)
    print(payload)
    print(SEP)

