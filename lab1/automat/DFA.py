import queue
from typing import Dict

from automat.NFA import NFA
from consts.constants import Consts
from preprocessing.RegexParser import RegexParser


class DFA:
    startState: int
    finishState: set
    stateDict: Dict[int, Dict[str, int]]

    def __init__(self, nfa: NFA):
        self.stateDict = {}
        self.finishState = set()

        self._create(nfa)
        self.minimize()

    def _create(self, nfa: NFA):
        stateDFAArr = []
        qState = queue.Queue()

        alphabet = nfa.getAlphabet()
        alphabet.discard(Consts.epsSymbol)

        startStateSet = {nfa.startState}

        startEpsStates = self._epsClosure(startStateSet, nfa)
        qState.put(startEpsStates)
        stateDFAArr.append(startEpsStates)
        self.startState = stateDFAArr.index(startEpsStates)
        while not qState.empty():
            curStateSet = qState.get()
            if self.getFinishState(curStateSet, nfa):
                self.finishState.add(stateDFAArr.index(curStateSet))

            for sign in alphabet:
                newStateSet = self._move(curStateSet, sign, nfa)
                epsClosureNew = self._epsClosure(newStateSet, nfa)
                if not len(newStateSet):
                    continue
                if epsClosureNew not in stateDFAArr:
                    qState.put(epsClosureNew)
                    stateDFAArr.append(epsClosureNew)

                iStart = stateDFAArr.index(curStateSet)
                iFinish = stateDFAArr.index(epsClosureNew)
                self.stateDict.setdefault(iStart, {})[sign] = iFinish

    def _epsClosure(self, stateSet, nfa):
        epsClosureSet = set()
        for state in stateSet:
            epsClosureSet.update(self._epsClosureState(state, nfa))
        return epsClosureSet

    def _epsClosureState(self, state, nfa):
        epsClosure = {state}
        toStateLst = nfa.stateDict.get(state, {}).get(Consts.epsSymbol, [])
        for state in toStateLst:
            epsClosure.update(self._epsClosureState(state, nfa))
        return epsClosure

    def _move(self, stateSet, sign, nfa):
        newStateSet = set()
        for state in stateSet:
            newStateSet.update(nfa.getGoalSetBySign(state, sign))
        return newStateSet

    def getFinishState(self, stateSet, nfa):
        for state in stateSet:
            if state in nfa.finishState:
                return True
        return False

    def accept(self, data: str):
        curState = self.startState
        for i in range(len(data)):
            print("|-{}".format(data[i:]), end='')
            toState = self.stateDict.get(curState, {}).get(data[i], None)
            if toState is None:
                print("|-недопуск")
                return False
            curState = toState

        if curState not in self.finishState:
            print("|-недопуск")
            return False
        print("|-допуск")
        return True

    def minimize(self):
        marked = self._buildTable()
        n = len(marked)
        component = [-1 for _ in range(n)]

        componentCnt = 0
        for i in range(n):
            if component[i] == -1:
                component[i] = componentCnt
                for j in range(i + 1, n):
                    if not marked[i][j]:
                        component[j] = componentCnt
                componentCnt += 1
        self.buildMinimization(component)

    def _buildTable(self):
        qState = queue.Queue()
        nState = len(self._getAllStates())
        marked = [[False for _ in range(nState)] for _ in range(nState)]
        alphabet = self._getAlphabet()

        for i in range(nState):
            isTerminalI = i in self.finishState
            for j in range(nState):
                isTerminalJ = j in self.finishState
                if not marked[i][j] and isTerminalI != isTerminalJ:
                    marked[i][j] = marked[j][i] = True
                    qState.put({i, j})

        while not qState.empty():
            statePair = list(qState.get())
            for sign in alphabet:
                for edge0 in self._getInverseEdges(statePair[0], sign):
                    for edge1 in self._getInverseEdges(statePair[1], sign):
                        if not marked[edge0][edge1]:
                            marked[edge0][edge1] = marked[edge1][edge0] = True
                            qState.put({edge0, edge1})
        return marked

    def _getInverseEdges(self, toState, sign):
        inverseEdgeArr = []
        for state, valueDict in self.stateDict.items():
            if sign in valueDict.keys():
                if valueDict[sign] == toState:
                    inverseEdgeArr.append(state)
        return inverseEdgeArr

    def _getAllStates(self):
        stateSet = set()
        for fromState, valueDict in self.stateDict.items():
            stateSet.add(fromState)
            for _, toState in valueDict.items():
                stateSet.add(toState)
        return stateSet

    def _getAlphabet(self):
        signArr = set()
        for _, valueDict in self.stateDict.items():
            signArr.update(valueDict.keys())
        return signArr

    def buildMinimization(self, component):
        newStateDict = {}
        for fromState, valueDict in self.stateDict.items():
            newFromState = component[fromState]
            for sign, toState in valueDict.items():
                newToState = component[toState]
                newStateDict.setdefault(newFromState, {})[sign] = newToState
        self.stateDict = newStateDict
        self.startState = component[self.startState]
        self.finishState = {component[state] for state in self.finishState}

    @staticmethod
    def createMinDFA(regex: str):
        resTree = RegexParser().parseExpression(regex)
        nfa = resTree.root.createNFA()

        return DFA(nfa)
