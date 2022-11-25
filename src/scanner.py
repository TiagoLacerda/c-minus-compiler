from dfa import DFA


"""
This file is dedicated to tokenizing source code written in the C-Minus language.
"""


def get_line_column(code: str, index: int):
    """
    Retrieve line and column equivalent of [index] in [code]. Lines break at newline character.

    Parameter [index] is zero-based. Line and Column are 1-based.

    Keyword arguments:
    code: a <str> representation of source code.
    index: index of a character in [code].
    """
    if index >= len(code):
        raise IndexError()

    line = 1
    column = 1
    for i in range(index):
        column += 1
        if code[i] == "\n":
            line += 1
            column = 1

    return line, column


# Load automaton
f = open("automata/complete.json", "r")
automaton = DFA.from_json(f.read())
f.close()

# Load source code
f = open("src/example.cminus", "r")
code = f.read()
f.close()

# Tokenize
tokens = []
start = 0
while start < len(code):
    state = automaton.initial_state
    final = -1
    tags = None
    for index in range(start, len(code)):
        letter = code[index]
        # If [letter] is any kind of whitespace (blankspace, newline, tab, ...), treat it as blankspace
        if letter.isspace():
            letter = " "

        if letter not in automaton.alphabet:
            line, column = get_line_column(code, index)
            raise ValueError(
                f"Unexpected symbol {letter} at line {line}, column {column}!")

        state = automaton.transitions[state][letter]

        if state in automaton.accept_states:
            final = index
            if state in automaton.tags.keys():
                tags = automaton.tags[state]

    if start > final:
        line, column = get_line_column(code, start)
        raise ValueError(
            f"Could't parse any token starting from line {line}, column {column}!")

    line, column = get_line_column(code, start)
    tokens.append([code[start:final + 1], tags, line, column])
    start = final + 1


# Replace keyword token types
keywords = {
    "else": ["else"],
    "if": ["if"],
    "int": ["int"],
    "return": ["return"],
    "void": ["void"],
    "while": ["while"]
}

for token in tokens:
    if (token[0] in keywords.keys()):
        token[1] = keywords[token[0]]

# Remove <blank> tokens
tokens = [token for token in tokens if "blank" not in token[1]]

# Print result as a minified string.
for i in range(len(tokens)):
    if (i % 2 == 0):
        print(f"\x1B[{94}m{tokens[i][0]}\x1B[0m", end="")
    else:
        print(f"\x1B[{91}m{tokens[i][0]}\x1B[0m", end="")
print("\n\n")

# Print result token by token, showing type
for i in range(len(tokens)):
    prefix = f"ln {tokens[i][2]}, cl {tokens[i][3]}: ".ljust(20)
    if (i % 2 == 0):
        print(f"\x1B[{94}m{prefix}{tokens[i][0].ljust(20)}{tokens[i][1]}\x1B[0m")
    else:
        print(f"\x1B[{91}m{prefix}{tokens[i][0].ljust(20)}{tokens[i][1]}\x1B[0m")
print("\n\n")
