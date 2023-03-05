import unittest

from preprocessing.RegexParser import RegexParser
from preprocessing.RegexTree import RegexTree


class testRegexParser(unittest.TestCase):
    def compareTrees(self, tree1: RegexTree, tree2: RegexTree):
        if tree1 is None and tree2 is None:
            return True

        return (tree1 is not None and tree2 is not None) and \
               (tree1.root.value == tree2.root.value) and \
               self.compareTrees(tree1.root.leftChild, tree2.root.leftChild) and \
               self.compareTrees(tree1.root.rightChild, tree2.root.rightChild)

    def treeToList(self, tree):
        curNode = tree.root
        stack = []
        path = ""
        res = []

        while True:
            if curNode is not None:
                stack.append((path, curNode))
                curNode = curNode.leftChild

                path += "L"
            elif len(stack):
                path, curNode = stack.pop()
                value = curNode.value

                res.append((path, value))
                curNode = curNode.rightChild

                path += "R"
            else:
                break
        return res

    def isEqualTrees(self, tree1, tree2):
        return self.treeToList(tree1) == tree2

    def test_parserOneElement(self):
        regex = "a"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [('', regex)]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserAnd(self):
        regex = "ab"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [('L', "a"), ('', "•"), ('R', "b")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserAndAnd(self):
        regex = "abc"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"), ("", "•"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserTwoElementAndSymbol(self):
        regex = "a•b"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [('L', "a"), ('', "•"), ('R', "b")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserOr(self):
        regex = "a|b"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [('L', "a"), ('', "|"), ('R', "b")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserOrOr(self):
        regex = "a|b|c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"), ("", "|"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserAndOr(self):
        regex = "ab|c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ('L', "•"), ("LR", "b"), ('', "|"), ('R', "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserOrAnd(self):
        regex = "a|bc"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ('', "|"), ("RL", "b"), ("R", "•"), ("RR", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserOrAndOr(self):
        regex = "a|bc|d"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LRL", "b"),
                    ("LR", "•"), ("LRR", "c"), ("", "|"),
                    ("R", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parserAndOrAnd(self):
        regex = "ab|cd"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "|"), ("RL", "c"), ("R", "•"),
                    ("RR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAndBracketsOr(self):
        regex = "a(b|c)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("RL", "b"),
                    ("R", "|"), ("RR", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAndBrackets(self):
        regex = "(ab)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("R", "b")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAnd_BracketsAnd(self):
        regex = "a(bc)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("RL", "b"),
                    ("R", "•"), ("RR", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsAnd_And(self):
        regex = "(ab)c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "•"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsOr_And(self):
        regex = "(a|b)c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"),
                    ("", "•"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsAnd_Or(self):
        regex = "(ab)|c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "|"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsOr_Or(self):
        regex = "(a|b)|c"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"),
                    ("", "|"), ("R", "c")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsAnd_And_BracketsAnd(self): #TODO уточнить строение
        regex = "(ab)(cd)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "•"), ("RL", "c"), ("R", "•"),
                    ("RR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsAnd_Or_BracketsAnd(self): #TODO уточнить строение
        regex = "(ab)|(cd)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "|"), ("RL", "c"), ("R", "•"),
                    ("RR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsOr_Or_BracketsOr(self): #TODO уточнить строение
        regex = "(a|b)|(c|d)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"),
                    ("", "|"), ("RL", "c"), ("R", "|"),
                    ("RR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsOr_And_BracketsOr(self): #TODO уточнить строение
        regex = "(a|b)(c|d)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"),
                    ("", "•"), ("RL", "c"), ("R", "|"),
                    ("RR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAnd_BracketsAnd_And_BracketsAnd(self): #TODO уточнить строение
        regex = "a(bc)(de)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LRL", "b"),
                    ("LR", "•"), ("LRR", "c"), ("", "•"),
                    ("RL", "d"), ("R", "•"), ("RR", "e")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAnd_BracketsAnd_Or_BracketsAnd(self): #TODO уточнить строение
        regex = "a(bc)|(de)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LRL", "b"),
                    ("LR", "•"), ("LRR", "c"), ("", "|"),
                    ("RL", "d"), ("R", "•"), ("RR", "e")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseOr_BracketsAnd_And_BracketsAnd(self):
        regex = "a|(bc)(de)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "|"), ("RLL", "b"),
                    ("RL", "•"), ("RLR", "c"), ("R", "•"),
                    ("RRL", "d"), ("RR", "•"), ("RRR", "e")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseOr_BracketsAnd_Or_BracketsAnd(self): #TODO уточнить строение
        regex = "a|(bc)|(de)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LRL", "b"),
                    ("LR", "•"), ("LRR", "c"), ("", "|"),
                    ("RL", "d"), ("R", "•"), ("RR", "e")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseOr_BracketsAnd_Or_AndBracketsOr(self): #TODO уточнить строение
        regex = "a|(bc)|d(e|f)"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LRL", "b"),
                    ("LR", "•"), ("LRR", "c"), ("", "|"),
                    ("RL", "d"), ("R", "•"), ("RRL", "e"),
                    ("RR", "|"), ("RRR", "f")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseAnd_BracketsOr_BracketsOr(self):
        regex = "a(b(c|d))"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("RL", "b"),
                    ("R", "•"), ("RRL", "c"), ("RR", "|"),
                    ("RRR", "d")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseStar(self):
        regex = "a*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseMultStar(self):
        regex = "ab*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("RL", "b"),
                    ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseStarMult(self):
        regex = "a*b"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "*"), ("", "•"),
                    ("R", "b")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseStarMultStar(self):
        regex = "a*b*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "*"), ("", "•"),
                    ("RL", "b"), ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsMilt_Star(self):
        regex = "(ab)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "•"), ("LR", "b"),
                    ("", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsOr_Star(self):
        regex = "(a|b)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "|"), ("LR", "b"),
                    ("", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseMult_BracketsAnd_Star(self):
        regex = "a(bc)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "•"), ("RLL", "b"),
                    ("RL", "•"), ("RLR", "c"), ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseOr_BracketsAnd_Star(self):
        regex = "a|(bc)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "|"), ("RLL", "b"),
                    ("RL", "•"), ("RLR", "c"), ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseOr_BracketsOr_Star(self):
        regex = "a|(b|c)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("L", "a"), ("", "|"), ("RLL", "b"),
                    ("RL", "|"), ("RLR", "c"), ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseStarAnd_BracketsAnd_Star(self):
        regex = "a*(bc)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "*"), ("", "•"),
                    ("RLL", "b"), ("RL", "•"), ("RLR", "c"),
                    ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseStarOr_BracketsOr_Star(self):
        regex = "a*|(b|c)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LL", "a"), ("L", "*"), ("", "|"),
                    ("RLL", "b"), ("RL", "|"), ("RLR", "c"),
                    ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsStarAnd_And_BracketsOr_Star(self):
        regex = "(a*b)(b|c)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LLL", "a"), ("LL", "*"), ("L", "•"),
                    ("LR", "b"), ("", "•"), ("RLL", "b"),
                    ("RL", "|"), ("RLR", "c"), ("R", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))

    def test_parseBracketsBracketsOrStarAndStar(self):
        regex = "((a|b)*c)*"
        resTree = RegexParser().parseExpression(regex)
        goalTree = [("LLLL", "a"), ("LLL", "|"), ("LLLR", "b"),
                    ("LL", "*"), ("L", "•"), ("LR", "c"),
                    ("", "*")]

        self.assertEqual(True, self.isEqualTrees(resTree, goalTree))


if __name__ == '__main__':
    unittest.main()
