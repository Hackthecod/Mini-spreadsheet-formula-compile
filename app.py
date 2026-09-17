import streamlit as st
import pandas as pd

from spreadsheet import Spreadsheet
from compiler_tree import get_tree_text


st.set_page_config(
    page_title="Mini Spreadsheet Compiler",
    page_icon="📊",
    layout="wide"
)


if "sheet" not in st.session_state:

    st.session_state.sheet = Spreadsheet()


if "data" not in st.session_state:

    st.session_state.data = {}


if "last_formula" not in st.session_state:

    st.session_state.last_formula = ""

st.title(
    "📊 Mini Spreadsheet Formula Compiler"
)


# SIDEBAR

with st.sidebar:

    st.header("Compiler")

    st.write(
        """
        This project demonstrates:

        1. Lexical Analysis
        2. Syntax Analysis
        3. AST Generation
        4. Semantic Analysis
        5. Formula Evaluation
        6. Error Detection
        7. Dependency Handling
        """
    )

    st.divider()

    st.subheader("Supported Functions")

    st.code(
        """
SUM(A1:A5)
AVG(A1:A5)
MAX(A1:A5)
MIN(A1:A5)
COUNT(A1:A5)
        """
    )


# CELL EDITOR

st.header("Spreadsheet")

st.write(
    "Enter values or formulas directly into the cells."
)


# Grid size
ROWS = 10
COLS = 8

columns = [
    chr(65 + i)
    for i in range(COLS)
]


# Create dataframe from current data
grid_data = []

for row in range(1, ROWS + 1):

    row_data = {}

    for col in columns:

        cell = f"{col}{row}"

        row_data[col] = (
            st.session_state.data.get(
                cell,
                ""
            )
        )

    grid_data.append(row_data)


df = pd.DataFrame(
    grid_data,
    index=range(1, ROWS + 1)
)


edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    key="spreadsheet_editor"
)


# UPDATE CELLS

for row in range(1, ROWS + 1):

    for col in columns:

        cell = f"{col}{row}"

        value = edited_df.loc[
            row,
            col
        ]

        if pd.isna(value):

            value = ""

        value = str(value)

        st.session_state.data[
            cell
        ] = value


# BUTTONS

col1, col2, col3 = st.columns(3)


# CALCULATE

with col1:

    calculate = st.button(
        "🧮 Calculate",
        use_container_width=True,
        type="primary"
    )


# COMPILER TREE

with col2:

    show_tree = st.button(
        "🌳 Compiler Tree",
        use_container_width=True
    )


# CLEAR

with col3:

    clear = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# CLEAR

if clear:

    st.session_state.data = {}

    st.session_state.sheet = Spreadsheet()

    st.session_state.last_formula = ""

    st.rerun()


# SAVE CURRENT DATA INTO SPREADSHEET

def update_spreadsheet():

    sheet = Spreadsheet()

    for cell, value in (
        st.session_state.data.items()
    ):

        if value != "":

            sheet.set_cell(
                cell,
                value
            )

    st.session_state.sheet = sheet

    return sheet


# CALCULATE

if calculate:

    sheet = update_spreadsheet()

    results = sheet.calculate_all()

    st.header("Calculation Results")

    result_rows = []

    for cell, value in results.items():

        raw = sheet.get_raw(cell)

        result_rows.append(
            {
                "Cell": cell,
                "Input / Formula": raw,
                "Result": value
            }
        )

    if result_rows:

        result_df = pd.DataFrame(
            result_rows
        )

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            "✓ Compilation and calculation completed."
        )

    else:

        st.info(
            "Enter some values or formulas first."
        )


# COMPILER TREE

if show_tree:

    sheet = update_spreadsheet()

    st.header(
        "🌳 Compiler Analysis"
    )

    formula_cells = []

    for cell, value in (
        st.session_state.data.items()
    ):

        if (
            isinstance(value, str)
            and value.startswith("=")
        ):

            formula_cells.append(cell)

    if not formula_cells:

        st.warning(
            "No formula found."
        )

        st.info(
            "Enter a formula such as "
            "=A1+B1*2"
        )

    else:

        selected_cell = st.selectbox(
            "Select formula cell",
            formula_cells
        )

        formula = sheet.get_raw(
            selected_cell
        )

        st.code(
            f"{selected_cell} = {formula}"
        )

        try:

            # LEXICAL + SYNTAX + AST

            tokens, ast, result = (
                sheet.evaluate_formula(
                    formula
                )
            )

            # PHASE 1

            st.subheader(
                "1️⃣ Lexical Analysis"
            )

            token_data = []

            for token_type, value in tokens:

                token_data.append(
                    {
                        "Token Type": token_type,
                        "Value": value
                    }
                )

            st.dataframe(
                pd.DataFrame(token_data),
                use_container_width=True,
                hide_index=True
            )

            # PHASE 2

            st.subheader(
                "2️⃣ Syntax Analysis"
            )

            tree = get_tree_text(
                ast
            )

            st.code(
                tree,
                language="text"
            )

            # PHASE 3

            st.subheader(
                "3️⃣ Semantic Analysis"
            )

            st.write(
                "Cell references are resolved "
                "and operations are checked."
            )

            # PHASE 4

            st.subheader(
                "4️⃣ Evaluation"
            )

            st.success(
                f"Result of {selected_cell}: "
                f"{result:g}"
            )

        except Exception as error:

            st.error(
                f"Compiler Error: {error}"
            )