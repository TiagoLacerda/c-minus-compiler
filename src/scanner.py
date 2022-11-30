from dfa import DFA
from token import Token


def get_line_column(string: str, index: int):
    """
    Retrieve line and column equivalent of [index] in [string]. Lines break at newline character.

    Parameter [index] is zero-based. Line and Column are 1-based.

    Keyword arguments:
    string: a <str> representation of source string.
    index: index of a character in [string].
    """
    if index >= len(string):
        raise IndexError()

    line = 1
    column = 1
    for i in range(index):
        column += 1
        if string[i] == "\n":
            line += 1
            column = 1

    return line, column


class Scanner:
    """
    Scanner.
    """

    def __init__(self, automaton: DFA):
        """
        Create a Scanner.

        Keyword arguments:
        automaton: a deterministic finite automaton that defines the language used to tokenize a given string.
        """
        self.automaton = automaton

    def scan(self, string: str):
        """
        Tokenize a [string].
        """

        # Tokenize
        tokens = []
        start = 0
        while start < len(string):
            # Reset scanning parameters
            state = self.automaton.initial_state  # Current automaton state
            final = -1  # Final index of current longest-acceptable-string
            tags = None  # Tags associated with current longest-acceptable-string

            # Scan whole string starting from [start]
            for index in range(start, len(string)):
                letter = string[index]

                # If [letter] is any kind of whitespace (blankspace, newline, tab, ...), treat it as blankspace
                if letter.isspace():
                    letter = " "

                # Error detection
                if letter not in self.automaton.alphabet:
                    line, column = get_line_column(string, index)
                    raise ValueError(
                        f"Unexpected symbol {letter} at line {line}, column {column}!")

                state = self.automaton.transitions[state][letter]

                if state in self.automaton.accept_states:
                    # Keep track of longest-acceptable-string
                    final = index
                    if state in self.automaton.tags.keys():
                        tags = self.automaton.tags[state]

            line, column = get_line_column(string, start)

            # Error detection
            if start > final:
                raise ValueError(
                    f"Could't parse any token starting from line {line}, column {column}!")

            # Instantiate token
            token = Token(string[start:final + 1], tags, line, column)

            # Error detection
            if len(token.tags) > 1:
                raise ValueError(
                    f"Ambiguity found in token {token.value}, starting from line {line}, column {column}: type can be {token.tags}")

            # Add token to tokens
            tokens.append(token)
            start = final + 1  # Start index of current longest-acceptable-string

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
            if (token.value in keywords.keys()):
                token.tags = keywords[token.value]

        # Remove <blank> tokens
        tokens = [token for token in tokens if "blank" not in token.tags]

        # Remove <comment> tokens
        tokens = [token for token in tokens if "comment" not in token.tags]

        return tokens
