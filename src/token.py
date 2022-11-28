import json


class Token:
    """
    Token.
    """

    def __init__(self, value: str, tags: list[str], line: int, column: int):
        """
        Create a Token.

        Keyword arguments:
        value: str value of the token.
        tags: possible token types associated with this token.
        line: line in source code [value] starts at.
        column: column in source code [value] starts at.
        """
        self.value = value
        self.tags = tags
        self.line = line
        self.column = column

    def __str__(self):
        return f"({self.value}, {self.tags}, {self.line}, {self.column})"

    def __eq__(self, other):
        return self.value == other.value and self.tags == other.tags and self.line == other.line and self.column == other.column

    def to_dict(self):
        """
        Returns an equivalent to this class instance as a <dict>.
        """
        return {
            "value": self.value,
            "tags": self.tags,
            "line": self.line,
            "column": self.column
        }

    def from_dict(data: dict):
        """
        Returns a class instance from an equivalent <dict>.
        """
        return Token(
            value=data["value"],
            tags=data["tags"],
            line=data["line"],
            column=data["column"]
        )

    def to_json(self):
        """
        Returns an equivalent to this class instance as a json <str>.
        """
        return json.dumps(self.to_dict())

    def from_json(data: str):
        """
        Returns a class instance from an equivalent json <str>.
        """
        return Token.from_dict(json.loads(data))
