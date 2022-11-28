import unittest

from src.dfa import DFA
from src.token import Token
from src.scanner import Scanner

"""
python -m unittest
"""


class TestScanner(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        f = open("automata/complete.json", "r")
        automaton = DFA.from_json(f.read())
        f.close()
        self.scanner = Scanner(automaton)

    @classmethod
    def tearDownClass(self):
        self.scanner = None

    def test_1(self):
        string = "/* this is a very nice comment */"
        tokens = [
            Token("/* this is a very nice comment */", ["comment"], 1, 1),
        ]
        self.assertEqual(tokens, self.scanner.scan(string))

    def test_2(self):
        string = "int main()"
        tokens = [
            Token("int", ["int"], 1, 1),
            Token("main", ["id"], 1, 5),
            Token("(", ["open_parenthesis"], 1, 9),
            Token(")", ["close_parenthesis"], 1, 10),
        ]
        self.assertEqual(tokens, self.scanner.scan(string))

    def test_3(self):
        string = "ç"
        self.assertRaises(ValueError, self.scanner.scan, string)
