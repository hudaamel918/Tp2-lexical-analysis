"""Prints the transition tables by querying the actual transition functions."""
from lexer_fa import identifier_step, number_step

def show(title, step, states, samples, accepting):
    print(title)
    print(f"{'State':8}" + "".join(f"{n:>16}" for n, _ in samples) + "   Accepting?")
    for s in states:
        row = "".join(f"{str(step(s, c) or 'REJECT'):>16}" for _, c in samples)
        print(f"{s:8}{row}   {'yes' if s in accepting else 'no'}")
    print()

show("Identifier DFA", identifier_step, ["q0", "q1"],
     [("letter", "a"), ("underscore", "_"), ("digit", "5"), ("other (-)", "-")], {"q1"})
show("Number DFA", number_step, ["q0", "q1", "q2", "q3"],
     [("digit", "7"), ("'.'", "."), ("other (a)", "a")], {"q1", "q3"})
