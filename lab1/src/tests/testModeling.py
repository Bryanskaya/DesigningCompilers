import unittest
from parameterized import parameterized

from automat.DFA import DFA


class TestModeling(unittest.TestCase):
    @parameterized.expand([
        ("emptyStr", "", False),
        ("a", "a", True),
        ("aaa", "aaa", False),
        ("ba", "ba", False),
        ("ac", "ac", False),
        ("1", "1", False)
    ])
    def test_acceptSingleSign(self, _, data, goal):
        regex = "a"
        dfa = DFA.createMinDFA(regex)

        res = dfa.accept(data)
        self.assertEqual(goal, res)

    @parameterized.expand([
        ("emptyStr", "", True),
        ("a", "a", True),
        ("aaa", "aaa", True),
        ("ba", "ba", False),
        ("ac", "ac", False),
        ("1", "1", False)
    ])
    def test_acceptStar(self, _, data, goal):
        regex = "a*"
        dfa = DFA.createMinDFA(regex)

        res = dfa.accept(data)
        self.assertEqual(goal, res)

    @parameterized.expand([
        ("emptyStr", "", False),
        ("a", "a", True),
        ("aa", "aa", False),
        ("b", "b", True),
        ("ab", "ab", False)
    ])
    def test_acceptOr(self, _, data, goal):
        regex = "a|b"
        dfa = DFA.createMinDFA(regex)

        res = dfa.accept(data)
        self.assertEqual(goal, res)

    @parameterized.expand([
        ("emptyStr", "", True),
        ("a", "a", False),
        ("aaa", "aaa", True),
        ("bab", "bab", True),
        ("babab", "babab", False),
        ("babaaa", "babaaa", True)
    ])
    def test_acceptBracketsOr_AndAnd_BracketsOr_Star(self, _, data, goal):
        regex = "((a|b)a(a|b))*"
        dfa = DFA.createMinDFA(regex)

        res = dfa.accept(data)
        self.assertEqual(goal, res)

    @parameterized.expand([
        ("emptyStr", "", False),
        ("a", "a", False),
        ("aabb", "aabb", True),
        ("bab", "bab", False),
        ("aaaaaaabb", "aaaaaaabb", True),
        ("aadbb", "aadbb", False),
        ("abb", "abb", True)
    ])
    def test_acceptBracketsOr_Star_AndAndAnd(self, _, data, goal):
        regex = "(a|b)*abb"
        dfa = DFA.createMinDFA(regex)

        res = dfa.accept(data)
        self.assertEqual(goal, res)


if __name__ == '__main__':
    unittest.main()
