import uuid
from automat.NFA import NFA


class Node:
    value: str
    leftChild = None
    rightChild = None

    def __init__(self, value, leftNode=None, rightNode=None):
        self.value = value
        self.leftChild = leftNode
        self.rightChild = rightNode

    def createNFA(self):
        leftNFA = self.leftChild.createNFA() if self.leftChild is not None else self.leftChild
        rightNFA = self.rightChild.createNFA() if self.rightChild is not None else self.rightChild
        return self._mergeNFA(leftNFA, rightNFA)

    def _mergeNFA(self, leftNFA, rightNFA):
        nfa = NFA()
        state1, state2 = str(uuid.uuid4()), str(uuid.uuid4())
        nfa.add(state1, state2, self.value)

        nfa.setStartState(state1)
        nfa.setFinishState(state2)

        return nfa
