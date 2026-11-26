"""Stage 2 (TP 2): Lexical analyzer based on finite automata.
No regular expressions are used anywhere in this file."""

KEYWORDS = {"int", "float", "double", "char", "void", "if", "else", "while", "for", "return"}
WHITESPACE = " \t\n\r\f\v"
TWO_CHAR_OPS = {"==", "!=", "<=", ">=", "&&", "||"}
ONE_CHAR_OPS = set("+-*/%=<>!")
SEPARATORS = set(";,(){}")


def is_letter(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def is_digit(c):
    return "0" <= c <= "9"


# ---------------------------------------------------------------- identifiers
def identifier_step(state, c):
    """Transition function of the identifier DFA. Returns next state or None (reject)."""
    if state == "q0":
        return "q1" if (is_letter(c) or c == "_") else None
    if state == "q1":
        return "q1" if (is_letter(c) or is_digit(c) or c == "_") else None
    return None


def is_identifier(word):
    """Validate a COMPLETE string with the identifier DFA."""
    state = "q0"
    for c in word:
        state = identifier_step(state, c)
        if state is None:
            return False
    return state == "q1"  # q1 is the only accepting state


def scan_identifier(src, i):
    """Run the identifier DFA from position i; return end index of the longest lexeme."""
    state, j = "q0", i
    while j < len(src):
        nxt = identifier_step(state, src[j])
        if nxt is None:
            break
        state, j = nxt, j + 1
    return j  # caller guarantees src[i] is letter or '_', so state == q1


# -------------------------------------------------------------------- numbers
def number_step(state, c):
    """Transition function of the number DFA. Returns next state or None (reject)."""
    if state == "q0":
        return "q1" if is_digit(c) else None
    if state == "q1":
        if is_digit(c):
            return "q1"
        return "q2" if c == "." else None
    if state == "q2":
        return "q3" if is_digit(c) else None
    if state == "q3":
        return "q3" if is_digit(c) else None
    return None


ACCEPTING = {"q1": "INTEGER", "q3": "REAL"}


def recognize_number(word):
    """Validate a COMPLETE string: returns 'INTEGER', 'REAL' or None."""
    if word == "":
        return None
    state = "q0"
    for c in word:
        state = number_step(state, c)
        if state is None:
            return None
    return ACCEPTING.get(state)


def scan_number(src, i):
    """Run the number DFA from i and return (end, type) of the LONGEST ACCEPTED prefix.
    If the automaton dies in q2 (e.g. '12.' or '12.x'), we fall back to the last
    accepting position (the integer '12'); the '.' is then reported separately."""
    state, j = "q0", i
    last_end, last_type = None, None
    while j < len(src):
        state = number_step(state, src[j])
        if state is None:
            break
        j += 1
        if state in ACCEPTING:
            last_end, last_type = j, ACCEPTING[state]
    return last_end, last_type


# -------------------------------------------------------------------- scanner
def lexical_analysis_fa(source_code):
    """Return a list of tokens (TYPE, lexeme, position) - same format as Stage 1."""
    tokens, i, n = [], 0, len(source_code)
    while i < n:
        c = source_code[i]
        if c in WHITESPACE:                       # skip whitespace
            i += 1
        elif is_letter(c) or c == "_":            # identifier / keyword
            j = scan_identifier(source_code, i)
            lexeme = source_code[i:j]
            tokens.append(("KEYWORD" if lexeme in KEYWORDS else "IDENTIFIER", lexeme, i))
            i = j
        elif is_digit(c):                         # integer / real
            j, kind = scan_number(source_code, i)
            tokens.append((kind, source_code[i:j], i))
            i = j
        elif source_code[i:i + 2] in TWO_CHAR_OPS:  # two-char operators FIRST
            tokens.append(("OPERATOR", source_code[i:i + 2], i))
            i += 2
        elif c in ONE_CHAR_OPS:
            tokens.append(("OPERATOR", c, i))
            i += 1
        elif c in SEPARATORS:
            tokens.append(("SEPARATOR", c, i))
            i += 1
        else:                                     # invalid character
            tokens.append(("INVALID", c, i))
            i += 1
    return tokens


if __name__ == "__main__":
    for t in lexical_analysis_fa("int total = 25;\nfloat average = 3.5;"):
        print(t)
