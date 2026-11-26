"""Stage 1 (TP 1): Lexical analyzer based on regular expressions."""
import re

KEYWORDS = {"int", "float", "double", "char", "void", "if", "else", "while", "for", "return"}

TOKEN_RE = re.compile(
    r"""
    (?P<WS>[ \t\n\r\f\v]+)
  | (?P<REAL>[0-9]+\.[0-9]+)
  | (?P<INTEGER>[0-9]+)
  | (?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<OP>==|!=|<=|>=|&&|\|\||[+\-*/%=<>!])
  | (?P<SEP>[;,(){}])
  | (?P<INVALID>.)
    """,
    re.VERBOSE | re.DOTALL,
)


def lexical_analysis_regex(source_code):
    """Return a list of tokens (TYPE, lexeme, position)."""
    tokens = []
    for m in TOKEN_RE.finditer(source_code):
        kind, text, pos = m.lastgroup, m.group(), m.start()
        if kind == "WS":
            continue
        if kind == "IDENT":
            kind = "KEYWORD" if text in KEYWORDS else "IDENTIFIER"
        elif kind == "OP":
            kind = "OPERATOR"
        elif kind == "SEP":
            kind = "SEPARATOR"
        tokens.append((kind, text, pos))
    return tokens


if __name__ == "__main__":
    for t in lexical_analysis_regex("int total = 25;\nfloat average = 3.5;"):
        print(t)
