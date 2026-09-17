from parser import (NumberNode, CellNode, BinaryOpNode, FunctionNode, RangeNode)

def build_tree(
    node,
    prefix="",
    is_last=True
):

    lines = []

    connector = (
        "└── "
        if is_last
        else "├── "
    )

    # Number
    if isinstance(node, NumberNode):

        lines.append(
            prefix
            + connector
            + f"NUMBER: {node.value:g}"
        )

    # Cell
    elif isinstance(node, CellNode):

        lines.append(
            prefix
            + connector
            + f"CELL: {node.name}"
        )

    # Operator
    elif isinstance(node, BinaryOpNode):

        lines.append(
            prefix
            + connector
            + f"OPERATOR: {node.operator}"
        )

        child_prefix = prefix + (
            "    "
            if is_last
            else "│   "
        )

        lines.extend(
            build_tree(
                node.left,
                child_prefix,
                False
            )
        )

        lines.extend(
            build_tree(
                node.right,
                child_prefix,
                True
            )
        )

    # Function
    elif isinstance(node, FunctionNode):

        lines.append(
            prefix
            + connector
            + f"FUNCTION: {node.name}"
        )

        child_prefix = prefix + (
            "    "
            if is_last
            else "│   "
        )

        for index, argument in enumerate(
            node.arguments
        ):

            last = (
                index
                == len(node.arguments) - 1
            )

            lines.extend(
                build_tree(
                    argument,
                    child_prefix,
                    last
                )
            )

    # Range
    elif isinstance(node, RangeNode):

        lines.append(
            prefix
            + connector
            + f"RANGE: "
            f"{node.start}:{node.end}"
        )

    return lines


def get_tree_text(ast):

    return "\n".join(
        build_tree(
            ast
        )
    )
