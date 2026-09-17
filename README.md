# Mini Spreadsheet Formula Compiler

A Compiler Design mini-project implemented using Python and Streamlit.

## Features

- Dynamic spreadsheet
- User-defined cell values
- User-defined formulas
- Cell references
- Arithmetic operators
- SUM()
- AVG()
- MAX()
- MIN()
- COUNT()
- Cell ranges
- Lexical analysis
- Syntax analysis
- Abstract Syntax Tree
- Semantic analysis
- Formula evaluation
- Circular reference detection
- Compiler tree visualization
- Error handling

## Project Structure

mini_spreadsheet/

├── app.py
├── lexer.py
├── parser.py
├── evaluator.py
├── spreadsheet.py
├── compiler_tree.py
├── requirements.txt
└── README.md

## Installation

Create a virtual environment:

python -m venv venv

Activate it.

Windows: venv\Scripts\activate

Linux/macOS: source venv/bin/activate

Install dependencies: pip install -r requirements.txt

## Run

streamlit run app.py

## Example

Enter:

A1 = 10
B1 = 20
C1 = =A1+B1

The result of C1 will be:

30

B1 = =SUM(A1:A3)

Result: 60

## Compiler Flow

Formula
    ↓
Lexical Analysis
    ↓
Tokens
    ↓
Syntax Analysis
    ↓
Abstract Syntax Tree
    ↓
Semantic Analysis
    ↓
Evaluation
    ↓
Result

## Example AST

Formula:

=A1+B1*2

AST:

        +
       / \
     A1   *
         / \
        B1  2

This demonstrates operator precedence.

## Compiler Concepts

### Lexical Analysis

The lexer converts the formula into tokens.

Example:

=A1+B1*2

becomes:

CELL A1
OPERATOR +
CELL B1
OPERATOR *
NUMBER 2

### Syntax Analysis

The parser checks whether the formula follows the grammar and generates an AST.

### Semantic Analysis

Cell references are resolved and invalid operations are detected.

### Evaluation

The AST is evaluated to produce the final spreadsheet value.

## Future Improvements

- IF() function
- AND() and OR()
- String values
- Formula bar
- Cell formatting
- Dependency graph
- Three-address code
- Export to CSV
- Import CSV
- More spreadsheet functions