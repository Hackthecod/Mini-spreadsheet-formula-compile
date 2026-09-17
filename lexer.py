import re


TOKEN_SPECIFICATION = [
    ("NUMBER",   r"\d+(?:\.\d+)?"),
    ("CELL",     r"[A-Za-z]+[0-9]+"),
    ("OPERATOR", r"[+\-*/^]"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("COMMA",    r","),
    ("COLON",    r":"),
    ("FUNCTION", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("SKIP",     r"[ \t]+"),
]


def tokenize(formula):
    """
    Lexical Analyzer.

    Converts:
        A1 + B1 * 10

    into:
        CELL(A1)
        OPERATOR(+)
        CELL(B1)
        OPERATOR(*)
        NUMBER(10)
    """

    tokens = []
    position = 0

    while position < len(formula):

        match = None

        for token_type, pattern in TOKEN_SPECIFICATION:

            regex = re.compile(pattern)
            match = regex.match(formula, position)

            if match:

                value = match.group(0)

                if token_type != "SKIP":

                    # Convert function names to uppercase
                    if token_type == "FUNCTION":
                        value = value.upper()

                    tokens.append(
                        (token_type, value)
                    )

                position = match.end()

                break

        if not match:

            raise SyntaxError(
                f"Invalid character '{formula[position]}' "
                f"at position {position}"
            )

    return tokens