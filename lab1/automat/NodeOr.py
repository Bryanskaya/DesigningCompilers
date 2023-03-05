import uuid

from automat.NFA import NFA
from automat.Node import Node
from consts.constants import Consts


class NodeOr(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.orSymbol, leftNode, rightNode)

    def _mergeNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        nfa.stateDict.update(leftNFA.stateDict)
        nfa.stateDict.update(rightNFA.stateDict)

        state1 = str(uuid.uuid4())
        state2 = str(uuid.uuid4())

        nfa.add(state1, leftNFA.startState, Consts.epsSymbol)
        nfa.add(state1, rightNFA.startState, Consts.epsSymbol)

        for finishState in leftNFA.finishState:
            nfa.add(finishState, state2, Consts.epsSymbol)
        for finishState in rightNFA.finishState:
            nfa.add(finishState, state2, Consts.epsSymbol)

        nfa.setStartState(state1)
        nfa.setFinishState(state2)

        return nfa
