from lexer import tokenize


# AST NODE CLASSES

class NumberNode:

    def __init__(self, value):
        self.value = float(value)


class CellNode:

    def __init__(self, name):
        self.name = name.upper()


class BinaryOpNode:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class FunctionNode:

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class RangeNode:

    def __init__(self, start, end):
        self.start = start
        self.end = end


# PARSER

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0

    def current(self):

        if self.position < len(self.tokens):
            return self.tokens[self.position]

        return None

    def eat(self, token_type):

        token = self.current()

        if token is None:

            raise SyntaxError(
                f"Expected {token_type}, "
                f"but reached end of formula"
            )

        if token[0] != token_type:

            raise SyntaxError(
                f"Expected {token_type}, "
                f"got {token}"
            )

        self.position += 1

        return token

    # expression

    def expression(self):

        node = self.term()

        while (
            self.current()
            and self.current()[1] in ("+", "-")
        ):

            operator = self.eat(
                "OPERATOR"
            )[1]

            right = self.term()

            node = BinaryOpNode(
                node,
                operator,
                right
            )

        return node

    # term

    def term(self):

        node = self.power()

        while (
            self.current()
            and self.current()[1] in ("*", "/")
        ):

            operator = self.eat(
                "OPERATOR"
            )[1]

            right = self.power()

            node = BinaryOpNode(
                node,
                operator,
                right
            )

        return node

    # power

    def power(self):

        node = self.factor()

        while (
            self.current()
            and self.current()[1] == "^"
        ):

            self.eat("OPERATOR")

            right = self.factor()

            node = BinaryOpNode(
                node,
                "^",
                right
            )

        return node

    # factor

    def factor(self):

        token = self.current()

        if token is None:

            raise SyntaxError(
                "Unexpected end of formula"
            )

        # Number
        if token[0] == "NUMBER":

            self.position += 1

            return NumberNode(
                token[1]
            )

        # Cell
        if token[0] == "CELL":

            self.position += 1

            return CellNode(
                token[1]
            )

        # Function
        if token[0] == "FUNCTION":

            return self.function()

        # Parentheses
        if token[0] == "LPAREN":

            self.eat("LPAREN")

            node = self.expression()

            self.eat("RPAREN")

            return node

        raise SyntaxError(
            f"Unexpected token: {token}"
        )

    # function

    def function(self):

        name = self.eat(
            "FUNCTION"
        )[1]

        self.eat("LPAREN")

        arguments = []

        if (
            self.current()
            and self.current()[0] != "RPAREN"
        ):

            arguments.append(
                self.argument()
            )

            while (
                self.current()
                and self.current()[0] == "COMMA"
            ):

                self.eat("COMMA")

                arguments.append(
                    self.argument()
                )

        self.eat("RPAREN")

        return FunctionNode(
            name,
            arguments
        )

    # function argument

    def argument(self):

        # Detect range:
        #
        # A1:A5

        if (
            self.current()
            and self.current()[0] == "CELL"
        ):

            start = self.eat(
                "CELL"
            )[1]

            if (
                self.current()
                and self.current()[0] == "COLON"
            ):

                self.eat("COLON")

                end = self.eat(
                    "CELL"
                )[1]

                return RangeNode(
                    start,
                    end
                )

            return CellNode(start)

        return self.expression()


# MAIN PARSER FUNCTION

def parse_formula(formula):

    tokens = tokenize(formula)

    parser = Parser(tokens)

    ast = parser.expression()

    if parser.current() is not None:

        raise SyntaxError(
            f"Unexpected token: "
            f"{parser.current()}"
        )

    return tokens, ast