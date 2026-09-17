import re

from parser import parse_formula
from evaluator import Evaluator


class Spreadsheet:

    def __init__(self):

        self.cells = {}

    # SET CELL

    def set_cell(self, cell, value):

        self.cells[
            cell.upper()
        ] = value

    # GET RAW CELL

    def get_raw(self, cell):

        return self.cells.get(
            cell.upper(),
            ""
        )

    # GET VALUE

    def get_value(
        self,
        cell,
        visited=None
    ):

        cell = cell.upper()

        if visited is None:

            visited = set()

        # Circular reference detection
        if cell in visited:

            raise ValueError(
                f"Circular reference detected at {cell}"
            )

        raw = self.get_raw(cell)

        # Empty cell
        if raw == "":

            return 0

        # Formula
        if isinstance(raw, str) and raw.startswith("="):

            visited.add(cell)

            formula = raw[1:]

            try:

                tokens, ast = parse_formula(
                    formula
                )

                evaluator = Evaluator(
                    self
                )

                result = evaluator.evaluate(
                    ast,
                    visited
                )

            finally:

                visited.remove(cell)

            return result

        # Number
        try:

            return float(raw)

        except ValueError:

            raise ValueError(
                f"Invalid value in cell {cell}: {raw}"
            )

    # EVALUATE FORMULA

    def evaluate_formula(
        self,
        formula
    ):

        if formula.startswith("="):

            formula = formula[1:]

        tokens, ast = parse_formula(
            formula
        )

        evaluator = Evaluator(
            self
        )

        result = evaluator.evaluate(
            ast
        )

        return tokens, ast, result

    # RANGE SUPPORT

    def expand_range(
        self,
        start,
        end
    ):

        start_col, start_row = self.split_cell(
            start
        )

        end_col, end_row = self.split_cell(
            end
        )

        cells = []

        for row in range(
            start_row,
            end_row + 1
        ):

            for col in range(
                self.column_to_number(start_col),
                self.column_to_number(end_col) + 1
            ):

                cells.append(
                    f"{self.number_to_column(col)}{row}"
                )

        return cells

    # CELL UTILITIES

    @staticmethod
    def split_cell(cell):

        match = re.match(
            r"([A-Za-z]+)([0-9]+)",
            cell
        )

        if not match:

            raise ValueError(
                f"Invalid cell reference: {cell}"
            )

        return (
            match.group(1).upper(),
            int(match.group(2))
        )

    @staticmethod
    def column_to_number(column):

        number = 0

        for char in column:

            number = (
                number * 26
                + ord(char) - ord("A") + 1
            )

        return number

    @staticmethod
    def number_to_column(number):

        result = ""

        while number > 0:

            number, remainder = divmod(
                number - 1,
                26
            )

            result = (
                chr(65 + remainder)
                + result
            )

        return result

    # GET ALL RESULTS

    def calculate_all(self):

        results = {}

        for cell in self.cells:

            try:

                results[cell] = self.get_value(
                    cell
                )

            except Exception as error:

                results[cell] = (
                    f"ERROR: {error}"
                )

        return results