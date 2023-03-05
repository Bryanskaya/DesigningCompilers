from typing import Dict, List


class NFA:
    stateDict: Dict[str, Dict[str, List[str]]]
    startState: str
    finishState: [str]

    def __init__(self):
        self.stateDict = {}
        self.finishState = []

    def add(self, startState, finishState, transition):
        if startState not in self.stateDict.keys():
            self.stateDict[startState] = {}
            self.stateDict[startState][transition] = [finishState]
        elif transition not in self.stateDict[startState].keys():
            self.stateDict[startState][transition] = [finishState]
        else:
            self.stateDict[startState][transition].append(finishState)

    def setStartState(self, startState: str):
        self.startState = startState

    def setFinishState(self, finishState: str):
        self.finishState.append(finishState)

    def getGoal(self, state):
        return self.stateDict[state]

    def getGoalSetBySign(self, state, sign):
        return set(self.stateDict.get(state, {}).get(sign, []))

    def popFinishState(self):
        finishStateArr = self.finishState
        self.finishState = []
        return finishStateArr

    def getAlphabet(self):
        signArr = set()
        for _, valueDict in self.stateDict.items():
            signArr.update(valueDict.keys())
        return signArr
