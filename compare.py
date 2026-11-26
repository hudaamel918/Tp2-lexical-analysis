"""Runs both analyzers on the same inputs, compares them, and benchmarks them."""
import re, timeit
from lexer_regex import lexical_analysis_regex
from lexer_fa import lexical_analysis_fa, is_identifier, recognize_number
from test_cases import VALID, INVALID, ALL


def fmt(tokens):
    return " ".join(f"{t[0]}({t[1]!r})" for t in tokens)


def main():
    print("=" * 70, "\nTEST RESULTS (token sequences)\n" + "=" * 70)
    rows = []
    for name, src in ALL.items():
        r, f = lexical_analysis_regex(src), lexical_analysis_fa(src)
        same = r == f
        rows.append((name, same, [t for t in f if t[0] == "INVALID"]))
        print(f"\n[{name}]  input = {src!r}")
        print("  regex :", fmt(r))
        print("  FA    :", fmt(f))
        print("  SAME  :", same)

    print("\n" + "=" * 70, "\nCOMPARISON TABLE\n" + "=" * 70)
    print(f"{'Test case':28} {'Equivalent?':12} Invalid characters detected (char@pos)")
    for name, same, inv in rows:
        print(f"{name:28} {'YES' if same else 'NO':12} {[(t[1], t[2]) for t in inv]}")
    print("\nAll equivalent:", all(r[1] for r in rows))

    print("\n" + "=" * 70, "\nWHOLE-STRING RECOGNIZERS (TP 2 sections 2 and 3)\n" + "=" * 70)
    for w in ["total", "_value", "x2", "2value", "total!", "", "total-x", "total2", "2total"]:
        print(f"is_identifier({w!r}) -> {is_identifier(w)}")
    for w in ["25", "100", "3.14", "0.5", "12.", ".5", "12a"]:
        print(f"recognize_number({w!r}) -> {recognize_number(w)}")

    print("\n" + "=" * 70, "\nCASES WHERE IMPLEMENTATIONS CAN DIFFER\n" + "=" * 70)
    # (a) Unicode-aware regex classes vs. explicit ASCII automaton
    uni = re.compile(r"\d+|\w+|\S")
    s = "x = \u0663;"
    print("Input:", repr(s))
    print("  regex using \\d/\\w :", uni.findall(s))
    print("  our FA (ASCII only):", [t[:2] for t in lexical_analysis_fa(s)])
    # (b) Wrong alternation order in a regex
    bad = re.compile(r"[0-9]+|[0-9]+\.[0-9]+|\.")
    print("Input: '3.14'")
    print("  regex with INTEGER before REAL:", bad.findall("3.14"))
    print("  our FA:", [t[:2] for t in lexical_analysis_fa("3.14")])

    print("\n" + "=" * 70, "\nBENCHMARK (pure CPython, 20 repeats)\n" + "=" * 70)
    big = "\n".join(VALID[k] for k in list(VALID)[:7]) * 400
    print("input size:", len(big), "characters")
    for label, fn in [("regex", lexical_analysis_regex), ("FA", lexical_analysis_fa)]:
        t = min(timeit.repeat(lambda: fn(big), number=1, repeat=20))
        print(f"  {label:6}: {t*1000:8.2f} ms")


if __name__ == "__main__":
    main()
