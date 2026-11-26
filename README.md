# TP 2 – Lexical Analysis Using Finite Automata

**Course:** Compiler Design – Practical Work (Undergraduate)
**Language:** Python 3 (standard library only)

This repository contains two lexical analyzers for the same small C-like language:

* **Stage 1 (TP 1)** – regular-expression based: `lexer_regex.py`
* **Stage 2 (TP 2)** – finite-automaton based, **no regular expressions**: `lexer_fa.py`

Both return a list of tokens `(TYPE, lexeme, position)`.
Token types: `KEYWORD`, `IDENTIFIER`, `INTEGER`, `REAL`, `OPERATOR`, `SEPARATOR`, `INVALID`.

## Repository structure

```
lexer_regex.py        Stage 1 – regex analyzer
lexer_fa.py           Stage 2 – finite-automaton analyzer (no `re`)
test_cases.py         Valid and invalid test programs shared by both analyzers
compare.py            Runs both analyzers, compares output, benchmarks
print_tables.py       Prints the transition tables from the real transition functions
results/
  transition_tables.txt
  test_results.txt    Full output of compare.py
README.md             This report
```

## How to run

```bash
python3 lexer_regex.py     # demo of Stage 1
python3 lexer_fa.py        # demo of Stage 2
python3 print_tables.py    # transition tables
python3 compare.py         # tests + comparison + benchmark
```

---

# Final Deliverables

## 1. Source code for both implementations

* Stage 1: [`lexer_regex.py`](lexer_regex.py) – one master regular expression with named groups. Order matters: `REAL` before `INTEGER`, two-character operators before one-character ones, and a catch-all `INVALID` group last.
* Stage 2: [`lexer_fa.py`](lexer_fa.py) – explicit transition functions `identifier_step` and `number_step`, plus the scanner `lexical_analysis_fa(source_code)`. It also contains the whole-string validators `is_identifier` and `recognize_number` from the assignment.

Key design point in Stage 2: `scan_number` remembers the **last accepting position**. For `12.` the automaton reaches the non-accepting state `q2` and then dies, so the scanner falls back to the last accepting state (`INTEGER 12`) and reports `.` separately as invalid. This is what makes the FA scanner behave exactly like the regex `[0-9]+\.[0-9]+ | [0-9]+` with longest-match semantics.

## 2. Finite-automaton transition tables

### Identifier DFA – regex `[A-Za-z_][A-Za-z0-9_]*`

Start state: `q0`. Accepting state: `q1`.

| State | letter | `_` | digit | other |
|-------|--------|-----|-------|-------|
| **q0** (start) | q1 | q1 | REJECT | REJECT |
| **q1** (accepting) | q1 | q1 | q1 | REJECT (stop; accept lexeme read so far) |

### Number DFA – integers `[0-9]+` and reals `[0-9]+\.[0-9]+`

Start state: `q0`. Accepting states: `q1` (INTEGER) and `q3` (REAL).

| State | digit | `.` | other |
|-------|-------|-----|-------|
| **q0** (start) | q1 | REJECT | REJECT |
| **q1** (accepting, INTEGER) | q1 | q2 | REJECT (stop; accept INTEGER) |
| **q2** (not accepting) | q3 | REJECT | REJECT |
| **q3** (accepting, REAL) | q3 | REJECT | REJECT (stop; accept REAL) |

(Generated from the real code by `print_tables.py`; see `results/transition_tables.txt`.)

## 3. Test results for valid and invalid inputs

Whole-string recognizers:

| Input | `is_identifier` | | Input | `recognize_number` |
|---|---|---|---|---|
| `total` | True | | `25` | INTEGER |
| `_value` | True | | `100` | INTEGER |
| `x2` | True | | `3.14` | REAL |
| `total2` | True | | `0.5` | REAL |
| `2value` | False | | `12.` | Rejected |
| `total!` | False | | `.5` | Rejected |
| `total-x` | False | | `12a` | Rejected |
| `""` | False | | | |

Scanner results (full token streams in `results/test_results.txt`):

| ID | Input | Tokens produced (identical for both analyzers) |
|----|-------|------------------------------------------------|
| V1 | `int total = 25;` / `float average = 3.5;` | KEYWORD(int) IDENTIFIER(total) OPERATOR(=) INTEGER(25) SEPARATOR(;) KEYWORD(float) IDENTIFIER(average) OPERATOR(=) REAL(3.5) SEPARATOR(;) |
| V2 | `x = (a + b2) * 3.14 - _tmp / 10;` | IDENTIFIER OPERATOR SEPARATOR IDENTIFIER OPERATOR IDENTIFIER SEPARATOR OPERATOR REAL(3.14) OPERATOR IDENTIFIER(_tmp) OPERATOR INTEGER(10) SEPARATOR |
| V3 | `if (x >= 10 && y != 0) { return x; } else { return 0; }` | `>=`, `&&`, `!=` recognized as single operators |
| V4 | `while (i <= 100) { i = i + 1; }` | `<=` recognized as a single operator |
| V5 | `a == b != c <= d >= e < f > g \|\| h && i ! j` | all two- and one-character operators |
| V6 | `0 7 100 0.5 3.14 25` | INTEGER, INTEGER, INTEGER, REAL, REAL, INTEGER |
| V7 | `x total _value value2 __ a_b_c` | six IDENTIFIER tokens |
| V8 | whitespace only | no tokens |
| I1 | `int x = 5 @ 3;` | … INTEGER(5) **INVALID(@ at pos 10)** INTEGER(3) … |
| I2 | `int 2value = 10;` | KEYWORD(int) INTEGER(2) IDENTIFIER(value) … (no syntax check at this phase) |
| I3 | `total-amount` | IDENTIFIER(total) OPERATOR(-) IDENTIFIER(amount) |
| I4 | `a # b $ c ~ d` | INVALID `#`@2, `$`@6, `~`@10 |
| I5 | `a & b \| c` | INVALID `&`@2, `\|`@6 (only `&&` and `\|\|` are operators) |
| I6 | `x = 12.;` | INTEGER(12) **INVALID(.)**@6 SEPARATOR(;) |
| I7 | `y = .5;` | **INVALID(.)**@4 INTEGER(5) |
| I8 | `12a 3.5abc` | INTEGER(12) IDENTIFIER(a) REAL(3.5) IDENTIFIER(abc) |
| I9 | `1.2.3` | REAL(1.2) INVALID(.) INTEGER(3) |
| I10 | `x = ٣;` (Arabic-Indic digit) | IDENTIFIER OPERATOR **INVALID(٣)** SEPARATOR |

## 4. Comparison table – are both implementations equivalent?

| Test case | Same tokens? | Invalid characters detected (both analyzers) |
|---|---|---|
| V1 – V8 (all valid programs) | **YES** | none |
| I1 at sign | YES | `@`@10 |
| I2 digit-first identifier | YES | none |
| I3 hyphen in word | YES | none |
| I4 bad symbols | YES | `#`@2, `$`@6, `~`@10 |
| I5 lone `&` and `\|` | YES | `&`@2, `\|`@6 |
| I6 trailing dot | YES | `.`@6 |
| I7 leading dot | YES | `.`@4 |
| I8 digits then letters | YES | none |
| I9 double dot | YES | `.`@3 |
| I10 Unicode digit | YES | `٣`@4 |

**Result: all 18 test programs produce identical token sequences and identical invalid-character reports** (`All equivalent: True`).

### Questions for comparison

**1. Do both analyzers produce the same tokens for all valid test programs?**
Yes. All eight valid programs (V1–V8) give exactly the same token list, including types, lexemes and positions. The two analyzers implement the same token definitions with the same longest-match and priority rules.

**2. Do both analyzers detect the same invalid characters?**
Yes. For every invalid test (I1–I10) both report the same characters at the same positions (e.g. `@` at 10, `#`/`$`/`~` at 2/6/10, lone `&` and `|`, a `.` that is not part of a real number, and a non-ASCII digit). Neither analyzer stops at an error; both report it and continue.

**3. What happens when an identifier begins with a digit?**
Neither analyzer accepts it as one identifier. In `2value` the digit starts a number, so both produce `INTEGER("2")` followed by `IDENTIFIER("value")`. The identifier DFA rejects a digit in `q0`, and the number DFA stops at the first non-digit. A lexical analyzer only splits the text into tokens; deciding that `int 2value = 10;` is an illegal declaration belongs to the parser (syntax analysis).

**4. How does each analyzer distinguish `123` from `12.3`?**
*Regex:* the alternative `REAL = [0-9]+\.[0-9]+` is listed **before** `INTEGER = [0-9]+`. At `12.3` REAL matches the whole string, while at `123` it fails (no `.`), so INTEGER matches.
*Finite automaton:* both are read by the same number DFA. `123` stays in `q1` (accepting, INTEGER). `12.3` goes `q0 → q1 → q2 → q3`, ends in `q3` (accepting, REAL). The final state decides the token type.

**5. Which implementation is easier to understand?**
It depends on what is being understood. The regex version is shorter (about 20 lines) and reads like a specification, so it is easier to read for people who know regular expressions. The FA version is easier to understand *how* recognition works, because every state, transition and accepting state is visible, and it can be traced by hand with the transition table. For learning, FA is clearer. For quickly reading what a token looks like, regex is clearer.

**6. Which implementation is easier to modify when a new token type is introduced?**
The regex version. A new token such as a string literal or a comment needs one new named group in the right priority position. In the FA version we must design new states and transitions (e.g. open quote, inside string, escape, closing quote), write a new `scan_*` function and add a new branch in the main loop. The FA approach is more work, but it gives full control, for example custom error messages for an unterminated string.

**7. Can you identify a case where both implementations behave differently? Explain why.**
With the final code on all 18 tests there is no difference, because both were written with the same ASCII-only definitions. Differences appear as soon as the two descriptions of the language are not exactly the same. `compare.py` demonstrates two real cases:

* **Unicode classes.** A regex written with `\d` / `\w` (Python 3 is Unicode-aware) accepts the Arabic-Indic digit `٣` as a digit/word character, while the FA, which tests `"0" <= c <= "9"`, rejects it as `INVALID`. Same idea, different character sets. This is why Stage 1 uses explicit `[0-9]` and `[A-Za-z_]`.
* **Alternation order.** With `[0-9]+|[0-9]+\.[0-9]+` (INTEGER before REAL) the regex engine takes the first alternative that matches and returns `['3', '.', '14']` for `3.14`, while the FA correctly returns `REAL('3.14')`. Regex alternation is *ordered*, not "longest", whereas the DFA always follows the longest path.
* A third source of difference is the *backtracking rule* in the FA: if `scan_number` stopped at the first failure instead of falling back to the last accepting state, `12.` would be rejected completely, while the regex would return `INTEGER(12)`. The FA code explicitly implements this fallback.

**8. Does a finite automaton necessarily run faster than a regular-expression implementation? Justify your answer.**
No. Measured on a 100,800-character input (pure CPython, best of 20 runs): **regex ≈ 20.8 ms, FA ≈ 23.7 ms** (numbers depend on the machine). In theory a DFA reads each character exactly once (O(n)), but speed depends on the implementation, not on the model. Python's `re` module runs in compiled C, while our FA is a Python loop where each character costs several interpreted function calls and comparisons. A table-driven DFA written in C or generated by tools like Lex/Flex would be much faster than both. Conversely, a regex engine that uses backtracking can be very slow on pathological patterns, while a DFA never backtracks over input. So: *a DFA has an excellent theoretical guarantee, but it is not automatically faster in practice.*

## 5. Report: advantages and limitations of each approach

**Regular expressions (Stage 1)**

*Advantages*
* Compact and declarative: the token definitions are visible in a few lines.
* Easy to add or change a token type (add a group, choose its priority).
* Runs in optimized C code inside Python's `re`, so it is fast with no extra effort.

*Limitations*
* Behavior depends on **ordering** of alternatives (REAL before INTEGER, `==` before `=`); a wrong order silently gives wrong tokens.
* Character classes can hide differences (`\d`, `\w` are Unicode-aware).
* The recognition process is hidden, so it is harder to see why something failed and to produce detailed error messages.
* Complex patterns become hard to read and can have poor worst-case behavior with backtracking engines.

**Finite automata (Stage 2)**

*Advantages*
* Every state and transition is explicit, so the algorithm can be traced, drawn and verified against the transition table.
* Precise control over error handling (we know exactly in which state the input failed).
* Single left-to-right pass, no backtracking over the input (except the controlled fallback to the last accepting state); this is the technique used by real lexer generators.

*Limitations*
* More code and more state management (about 3x longer).
* Adding or changing a token means redesigning states and transitions, and bugs in transitions are easy to introduce.
* In pure Python it is not faster than `re`.
* Hand-written automata do not scale well to many token types; real compilers generate them automatically from regular expressions.

**Common limitation:** both only recognize token patterns. Neither checks syntax; `int 2value = 10;` is tokenized without error and must be rejected by the parser.

**Conclusion.** Regular expressions and finite automata describe the same class of languages (regular languages). A regular expression is a compact *description*; a finite automaton is the explicit *recognition procedure*. Our tests confirm that, when both are defined with the same rules, they produce identical results. Real compilers combine both ideas: tokens are specified with regular expressions and converted automatically (regex → NFA → DFA) into an efficient automaton.

---

# Appendix – Answers to the in-text questions of the assignment

**Section 2 (identifiers)**
1. `total2` is valid: it starts with a letter (`q0 → q1`) and the remaining characters are letters/digits, which keep the DFA in `q1`.
2. `2total` is invalid: the first character is a digit and `q0` has no transition on a digit, so it is rejected immediately.
3. The accepting state is `q1`.
4. A hyphen has no transition in `q0` or `q1`, so the automaton rejects it. Inside a larger program the scanner stops the identifier before the hyphen and treats `-` as an operator (`total-amount` → IDENTIFIER, OPERATOR, IDENTIFIER).

**Section 4 (scanner)**
1. Identifiers (and numbers) are tested first because "invalid character" is the fallback: it is chosen only when no valid token can start at the current character. Testing it first would wrongly flag valid characters.
2. The accepting state of the identifier automaton is `q1` only.
3. `3.5` ends in `q3`, which is the accepting state for numbers with a decimal point (REAL); an integer ends in `q1`.
4. `@` matches no token pattern, so the scanner emits `INVALID('@')` with its position and continues with the next character.
5. Two-character operators (`==`, `<=`, `>=`, `!=`, `&&`, `||`) must be checked first; otherwise `==` would be read as two `=` tokens (and `<=` as `<` then `=`). This is the longest-match rule.
6. Yes, both analyzers produce the same sequence (see comparison table above).
