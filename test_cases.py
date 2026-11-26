"""Shared test programs (valid and invalid inputs)."""
VALID = {
    "V1 declarations": "int total = 25;\nfloat average = 3.5;",
    "V2 expression": "x = (a + b2) * 3.14 - _tmp / 10;",
    "V3 if/else": "if (x >= 10 && y != 0) { return x; } else { return 0; }",
    "V4 while loop": "while (i <= 100) { i = i + 1; }",
    "V5 operators": "a == b != c <= d >= e < f > g || h && i ! j",
    "V6 numbers": "0 7 100 0.5 3.14 25",
    "V7 identifiers": "x total _value value2 __ a_b_c",
    "V8 empty / blank": "   \n\t  ",
}
INVALID = {
    "I1 at sign": "int x = 5 @ 3;",
    "I2 digit-first identifier": "int 2value = 10;",
    "I3 hyphen in word": "total-amount",
    "I4 bad symbols": "a # b $ c ~ d",
    "I5 lone & and |": "a & b | c",
    "I6 trailing dot": "x = 12.;",
    "I7 leading dot": "y = .5;",
    "I8 digits then letters": "12a 3.5abc",
    "I9 double dot": "1.2.3",
    "I10 Unicode digit": "x = \u0663;",
}
ALL = {**VALID, **INVALID}
