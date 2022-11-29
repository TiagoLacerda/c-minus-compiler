import json
import sys

from dfa import DFA
from token import Token
from scanner import Scanner

"""
This file is dedicated to scanning and parsing source code written in the C-Minus language.

Usage:
python ./src/compiler.py <source> <destination> -d (debug?) -v (verbose?) -o (output to .json file?)

-d: Whether the program should print the result to the console.

-v: Whether printed information should be verbose or minified.

-o: Whether the program should write the result to <destination> file.

Known issues:
If directory of <destination> does not yet exists, an error is thrown, instead of creating it.
"""


def print_verbose(tokens: list[Token]):
    """
    Print detailed information of each token, line by line.
    """
    paddings = [0 for i in range(4)]
    for token in tokens:
        paddings[0] = max(paddings[0], len(str(token.line)))
        paddings[1] = max(paddings[1], len(str(token.column)))
        paddings[2] = max(paddings[2], len(str(token.value)))
        paddings[3] = max(paddings[3], len(str(token.tags)))

    highlight = False  # Highlight every other token
    for token in tokens:
        line = str(token.line).ljust(paddings[0])
        column = str(token.column).ljust(paddings[1])
        value = str(token.value).ljust(paddings[2])
        tags = str(token.tags).ljust(paddings[3])

        info = f"ln {line}, cl {column}: {value} {tags}"
        code = 94 if highlight else 91
        highlight = not highlight
        print(f"\x1B[{code}m{info}\x1B[0m")


def print_minified(tokens: list[Token]):
    """
    Print token values as a minified string.
    """
    highlight = False  # Highlight every other token
    for token in tokens:
        info = str(token.value)
        code = 94 if highlight else 91
        highlight = not highlight
        print(f"\x1B[{code}m{info}\x1B[0m", end="")
    print("")


# Validate arguments
if len(sys.argv) < 2:
    raise RuntimeError("Not enough arguments!")

if len(sys.argv) > 6:
    raise RuntimeError("Too many arguments!")

# Load Scanner automaton
f = open("automata/complete.json", "r")
automaton = DFA.from_json(f.read())
f.close()

# Instantiate scanner
scanner = Scanner(automaton)

# Load source code
f = open(sys.argv[1], "r")
code = f.read()
f.close()

# Tokenize source code
tokens = scanner.scan(code)

if "-d" in sys.argv:
    # Print tokens to console
    if "-v" in sys.argv:
        # Detailed
        print_verbose(tokens)
    else:
        # Minified
        print_minified(tokens)

if "-o" in sys.argv:
    # Output tokens to .json file
    f = open(sys.argv[2], "w")
    f.write(json.dumps({"tokens": [token.to_dict() for token in tokens]}))
    f.close()
