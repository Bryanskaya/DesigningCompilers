from automat.NFA import NFA
from automat.Node import Node
from consts.constants import Consts


class NodeAnd(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.andSymbol, leftNode, rightNode)

    def _mergeNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        nfa.stateDict.update(leftNFA.stateDict)
        nfa.stateDict.update(rightNFA.stateDict)

        for finishState in leftNFA.finishState:
            nfa.add(finishState, rightNFA.startState, Consts.epsSymbol)

        nfa.setStartState(leftNFA.startState)
        for finishState in rightNFA.finishState:
            nfa.setFinishState(finishState)

        return nfa
