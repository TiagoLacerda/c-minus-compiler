from dfa import DFA


"""
This file is dedicated to the creation of Deterministic Finite Automata for each token type of the C-Minus language.

"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
"+", "-", "*", "/", "<", ">", "=", "!",
"(", ")", "[", "]", "{", "}",
",", ";"
"""


def generate_id():
    """
    Generate a Deterministic Finite Automaton that accepts identifiers as defined in the C-Minus BNF.

    Save a Json representation of the DFA in "automata/id.json".
    """
    states = [
        "0",
        "1"
    ]

    alphabet = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    ]

    transitions = {}
    for state in states:
        transitions[state] = {}
        for letter in alphabet:
            transitions[state][letter] = "1"

    initial_state = "0"

    accept_states = ["1"]
    tags = {"1": ["id"]}

    automaton = DFA(
        states,
        alphabet,
        transitions,
        initial_state,
        accept_states,
        tags
    )

    f = open("./automata/id.json", "w")
    f.write(automaton.to_json())
    f.close()


def generate_num():
    """
    Generate a Deterministic Finite Automaton that accepts numbers as defined in the C-Minus BNF.

    Save a Json representation of the DFA in "automata/num.json".
    """
    states = [
        "0",
        "1"
    ]

    alphabet = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ]

    transitions = {}
    for state in states:
        transitions[state] = {}
        for letter in alphabet:
            transitions[state][letter] = "1"

    initial_state = "0"

    accept_states = ["1"]
    tags = {"1": ["num"]}

    automaton = DFA(
        states,
        alphabet,
        transitions,
        initial_state,
        accept_states,
        tags
    )

    f = open("automata/num.json", "w")
    f.write(automaton.to_json())
    f.close()


def generate_eq():
    """
    Generate a Deterministic Finite Automaton that accepts equality operator "==" as defined in the C-Minus BNF.

    Save a Json representation of the DFA in "automata/eq.json".
    """
    states = [
        "0",
        "1",
        "2",
        "3"
    ]

    alphabet = [
        "="
    ]

    transitions = {
        "0": {
            "=": "1"
        },
        "1": {
            "=": "2"
        },
        "2": {
            "=": "3"
        },
        "3": {
            "=": "3"
        }
    }

    initial_state = "0"

    accept_states = ["2"]
    tags = {"2": ["eq"]}

    automaton = DFA(
        states,
        alphabet,
        transitions,
        initial_state,
        accept_states,
        tags
    )

    f = open("automata/eq.json", "w")
    f.write(automaton.to_json())
    f.close()


def generate_single_letter(letter: str, tag: str):
    """
    Generate a Deterministic Finite Automaton that accepts single-character tokens as defined in the C-Minus BNF.

    Save a Json representation of the DFA in "automata/[tag].json".
    """
    states = [
        "0",
        "1",
        "2"
    ]

    alphabet = [
        letter
    ]

    transitions = {
        "0": {
            letter: "1"
        },
        "1": {
            letter: "2"
        },
        "2": {
            letter: "2"
        },
    }

    initial_state = "0"
    accept_states = ["1"]
    tags = {"1": [tag]}

    automaton = DFA(
        states,
        alphabet,
        transitions,
        initial_state,
        accept_states,
        tags
    )

    f = open(f"automata/{tag}.json", "w")
    f.write(automaton.to_json())
    f.close()


def generate_double_letter(first: str, second: str, tag: str):
    """
    Generate a Deterministic Finite Automaton that accepts double-character tokens as defined in the C-Minus BNF.

    Save a Json representation of the DFA in "automata/[tag].json".
    """
    states = [
        "0",
        "1",
        "2",
        "3"
    ]

    alphabet = list(set([first, second]))

    transitions = {
        "0": {
            first: "1",
            second: "3"
        },
        "1": {
            first: "3",
            second: "2"
        },
        "2": {
            first: "3",
            second: "3"
        },
        "3": {
            first: "3",
            second: "3"
        }
    }

    initial_state = "0"
    accept_states = ["2"]
    tags = {"2": [tag]}

    automaton = DFA(
        states,
        alphabet,
        transitions,
        initial_state,
        accept_states,
        tags
    )

    f = open(f"automata/{tag}.json", "w")
    f.write(automaton.to_json())
    f.close()


# Generate automaton for recognizing identifiers
generate_id()

# Generate automaton for recognizing numbers
generate_num()

# Generate automaton for recognizing equality operator
generate_eq()

# Automatize single-character automata creation
map = {
    " ": "blank",
    "+": "plus",
    "-": "minus",
    "*": "asterisk",
    "/": "slash",
    "<": "lt",
    ">": "gt",
    "=": "assign",
    ";": "semicolon",
    ",": "comma",
    "(": "open_parenthesis",
    ")": "close_parenthesis",
    "[": "open_square_brackets",
    "]": "close_square_brackets",
    "{": "open_brackets",
    "}": "close_brackets",
}

# Generate automata for recognizing single-character tokens (plus, minus, ...)
for letter in map.keys():
    generate_single_letter(letter, map[letter])

# Automatize double-character automata creation
map = {
    "!=": "ne",
    "<=": "le",
    ">=": "ge",
    "/*": "open_comment",
    "*/": "close_comment",
}

# Generate automata for recognizing double-character tokens (le, ge, ne, ...)
for letters in map.keys():
    generate_double_letter(letters[0], letters[1], map[letters])


# Generate automaton equivalent to the union of all others
f = open("automata/id.json", "r")
id = DFA.from_json(f.read())
f.close()

f = open("automata/num.json", "r")
num = DFA.from_json(f.read())
f.close()

dfa = id.union(num).remove_unreachable_states()

filenames = [
    # Single-character
    "automata/blank.json",
    "automata/plus.json",
    "automata/minus.json",
    "automata/asterisk.json",
    "automata/slash.json",
    "automata/lt.json",
    "automata/gt.json",
    "automata/assign.json",
    "automata/semicolon.json",
    "automata/comma.json",
    "automata/open_parenthesis.json",
    "automata/close_parenthesis.json",
    "automata/open_square_brackets.json",
    "automata/close_square_brackets.json",
    "automata/open_brackets.json",
    "automata/close_brackets.json",
    # Double-character
    "automata/eq.json",
    "automata/ne.json",
    "automata/le.json",
    "automata/ge.json",
    "automata/open_comment.json",
    "automata/close_comment.json",
]

for filename in filenames:
    f = open(filename, "r")
    other = DFA.from_json(f.read())
    f.close()

    dfa = dfa.union(other).remove_unreachable_states()

f = open("automata/complete.json", "w")
f.write(dfa.to_json())
f.close()
