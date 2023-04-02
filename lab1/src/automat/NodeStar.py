import uuid

from automat.NFA import NFA
from automat.Node import Node
from consts.constants import Consts


class NodeStar(Node):
    def __init__(self, leftNode=None, rightNode=None):
        super().__init__(Consts.starSymbol, leftNode, rightNode)

    def _mergeNFA(self, leftNFA, rightNFA):
        nfa = NFA()

        nfa.stateDict.update(leftNFA.stateDict)

        state1 = str(uuid.uuid4())
        state2 = str(uuid.uuid4())

        nfa.add(state1, leftNFA.startState, Consts.epsSymbol)
        nfa.add(state1, state2, Consts.epsSymbol)
        for finishState in leftNFA.finishState:
            nfa.add(finishState, leftNFA.startState, Consts.epsSymbol)
            nfa.add(finishState, state2, Consts.epsSymbol)

        nfa.setStartState(state1)
        nfa.setFinishState(state2)

        return nfa
