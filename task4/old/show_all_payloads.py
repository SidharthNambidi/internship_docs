from payloads import build_payload, CARRIERS, DIRECTIVES

SEP = "=" * 70
COPIES_LEVELS = [1, 2, 4, 8]

output_lines = []


def emit(line=""):
    print(line)
    output_lines.append(line)


for carrier in CARRIERS:
    for directive in DIRECTIVES:
        for forged in [False, True]:
            for copies in COPIES_LEVELS:
                payload = build_payload(carrier, directive, forged, copies)
                emit("\n" + SEP)
                emit(f"CARRIER={carrier}  DIRECTIVE={directive}  "
                     f"FORGED={forged}  COPIES={copies}")
                emit(SEP)
                emit(payload)

emit("\nTotal combinations generated: "
     f"{len(CARRIERS) * len(DIRECTIVES) * 2 * len(COPIES_LEVELS)}")

with open("all_payloads.txt", "w") as f:
    f.write("\n".join(output_lines))

print("\nSaved full listing to all_payloads.txt")
