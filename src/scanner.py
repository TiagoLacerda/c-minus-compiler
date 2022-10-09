from dfa import DFA


"""
This file is dedicated to tokenizing source code written in the C-Minus language.
"""


# Load automaton
f = open("automata/complete.json", "r")
automaton = DFA.from_json(f.read())
f.close()

# Load source code
f = open("src/example.cminus", "r")
# code = "_".join(f.read().split())
code = "".join(f.read().split())
f.close()

# Tokenize
tokens = []
start = 0
index = 0
tags = None
state = automaton.initial_state
while index < len(code):
    letter = code[index]
    if letter not in automaton.alphabet:
        raise ValueError(f"Unexpected symbol \"{letter}\"!")

    state = automaton.transitions[state][letter]

    if state in automaton.accept_states:
        if state in automaton.tags.keys():
            tags = automaton.tags[state]
    else:
        if tags == None:
            raise ValueError("Could not parse source code!")
        else:
            tokens.append([code[start:index], tags])
            state = automaton.initial_state
            start = index
            index -= 1
            tags = None
    index += 1

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
# tokens = [token for token in tokens if "blank" not in token[1]]

# Print result as a minified string.
for i in range(len(tokens)):
    if (i % 2 == 0):
        print(f"\x1B[{94}m{tokens[i][0]}\x1B[0m", end="")
    else:
        print(f"\x1B[{91}m{tokens[i][0]}\x1B[0m", end="")
print("\n\n")

# Print result token by token, showing type
for i in range(len(tokens)):
    if (i % 2 == 0):
        print(f"\x1B[{94}m{tokens[i][0].ljust(8)}{tokens[i][1]}\x1B[0m")
    else:
        print(f"\x1B[{91}m{tokens[i][0].ljust(8)}{tokens[i][1]}\x1B[0m")
print("\n\n")
