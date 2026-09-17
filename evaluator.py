from parser import (NumberNode, CellNode, BinaryOpNode, FunctionNode, RangeNode)

class Evaluator:

    def __init__(self, spreadsheet):

        self.spreadsheet = spreadsheet

    # EVALUATE AST

    def evaluate(
        self,
        node,
        visited=None
    ):

        if visited is None:
            visited = set()

        # NUMBER

        if isinstance(node, NumberNode):

            return node.value

        # CELL

        if isinstance(node, CellNode):

            return self.spreadsheet.get_value(
                node.name,
                visited
            )

        # BINARY OPERATION

        if isinstance(node, BinaryOpNode):

            left = self.evaluate(
                node.left,
                visited
            )

            right = self.evaluate(
                node.right,
                visited
            )

            if node.operator == "+":

                return left + right

            if node.operator == "-":

                return left - right

            if node.operator == "*":

                return left * right

            if node.operator == "/":

                if right == 0:

                    raise ZeroDivisionError(
                        "Division by zero"
                    )

                return left / right

            if node.operator == "^":

                return left ** right

            raise ValueError(
                f"Unknown operator "
                f"{node.operator}"
            )

        # RANGE

        if isinstance(node, RangeNode):

            cells = self.spreadsheet.expand_range(
                node.start,
                node.end
            )

            return [
                self.spreadsheet.get_value(
                    cell,
                    visited
                )
                for cell in cells
            ]

        # FUNCTION

        if isinstance(node, FunctionNode):

            values = []

            for argument in node.arguments:

                value = self.evaluate(
                    argument,
                    visited
                )

                # Flatten ranges
                if isinstance(value, list):

                    values.extend(value)

                else:

                    values.append(value)

            if node.name == "SUM":

                return sum(values)

            if node.name == "AVG":

                if not values:
                    return 0

                return sum(values) / len(values)

            if node.name == "MAX":

                if not values:
                    return 0

                return max(values)

            if node.name == "MIN":

                if not values:
                    return 0

                return min(values)

            if node.name == "COUNT":

                return len(values)

            raise ValueError(
                f"Unknown function: {node.name}"
            )

        raise ValueError(
            "Unknown AST node"
        )