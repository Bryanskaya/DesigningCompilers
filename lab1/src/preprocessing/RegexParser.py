from automat.NodeAnd import NodeAnd
from automat.NodeOr import NodeOr
from automat.NodeStar import NodeStar
from automat.Node import Node
from consts.constants import Consts
from preprocessing.RegexTree import RegexTree


class RegexParser:
    i = 0
    stackBrackets = 0

    def parseExpression(self, regexStr: str):
        regexStr = regexStr.replace(" ", "")
        res = self.parse(regexStr)
        return self.buildTree(res)

    def buildTree(self, node: list):
        tree = RegexTree()
        tree.root = node
        return tree

    def parse(self, regexStr: str):
        nodeArr = self._createNodeLst(regexStr)
        return self._buildTreeNode(nodeArr)

    def _createNodeLst(self, regexStr: str):
        nodeLst = []
        while self.i < len(regexStr) and regexStr[self.i] != Consts.closeSymbol:
            nodeLst.append(self._createNode(regexStr))
            self.i += 1
        return nodeLst

    def _createNode(self, regexStr):
        elem = regexStr[self.i]

        if elem not in Consts.allControlSymbols:  # not (,),*,|,•
            return Node(elem)
        if elem in Consts.allOperators:  # *,|,•
            return elem
        if elem == Consts.openSymbol:
            self.i += 1
            return self.parse(regexStr)
        if elem == Consts.closeSymbol:
            return

    def _buildTreeNode(self, nodeLst: list):
        nodeLst = self._parseStar(nodeLst)
        nodeLst = self._parseAnd(nodeLst)
        nodeLst = self._parseOr(nodeLst)

        if len(nodeLst) != 1:
            raise Exception("Ошибка в процессе построения дерева: больше, чем 1 элемент в массиве")

        return nodeLst[0]

    def _parseStar(self, nodeLst):
        updLst = []
        for i in range(len(nodeLst)):
            node = nodeLst[i]

            if node == Consts.starSymbol:
                if i == 0:
                    raise Exception("Ошибка: неверная постановка символа *")

                node = NodeStar(updLst.pop())
            updLst.append(node)

        return updLst

    def _parseAnd(self, nodeLst):
        i = 0
        updLst = []
        isPreviousNode = False

        while i < len(nodeLst):
            node = nodeLst[i]

            if node == Consts.andSymbol:
                if i == 0 or i == len(nodeLst) - 1 or \
                        nodeLst[i - 1] in [Consts.orSymbol, Consts.andSymbol, Consts.openSymbol] or \
                        nodeLst[i + 1] in [Consts.orSymbol, Consts.andSymbol, Consts.closeSymbol, Consts.starSymbol]:
                    raise Exception("Ошибка: неверная постановка символа •")

                node = NodeAnd(updLst.pop(), nodeLst[i + 1])
                i += 1
                isPreviousNode = False
            elif isinstance(node, Node):
                if isPreviousNode:
                    node = NodeAnd(updLst.pop(), node)
                isPreviousNode = True
            else:
                isPreviousNode = False
            updLst.append(node)

            i += 1
        return updLst

    def _parseOr(self, nodeLst: list):
        i = 0
        updLst = []

        while i < len(nodeLst):
            node = nodeLst[i]

            if node == Consts.orSymbol:
                if i == 0 or i == len(nodeLst) - 1 or \
                        nodeLst[i - 1] in [Consts.orSymbol, Consts.andSymbol, Consts.openSymbol] or \
                        nodeLst[i + 1] in [Consts.orSymbol, Consts.andSymbol, Consts.closeSymbol, Consts.starSymbol]:
                    raise Exception("Ошибка: неверная постановка символа |")
                node = NodeOr(updLst.pop(), nodeLst[i + 1])
                i += 1
            updLst.append(node)
            i += 1

        return updLst
