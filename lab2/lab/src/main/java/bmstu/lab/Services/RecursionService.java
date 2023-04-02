package bmstu.lab.Services;

import bmstu.lab.Entities.GrammarInfo;
import bmstu.lab.Entities.Rule;
import bmstu.lab.Entities.Symbol;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.Executors;

@Slf4j
public class RecursionService {
    public void deleteLeftRecursion(GrammarInfo grammarInfo) throws Exception {
        for (int i = 0; i < grammarInfo.nonTerminalSymbols.size(); i++) {
            String nonTerminalI = grammarInfo.nonTerminalSymbols.get(i);

            for (int j = 0; j < i; j ++) {
                String nonTerminalJ = grammarInfo.nonTerminalSymbols.get(j);

                expandRules(nonTerminalI, nonTerminalJ, grammarInfo.productions);
            }

            deleteRecursion(grammarInfo.productions, nonTerminalI);
        }
    }

    private void expandRules(String leftNonTerminal, String rightNonTerminal, List<Rule> ruleList) {
        int i = 0;
        while (i < ruleList.size()) {
            Rule curRule = ruleList.get(i);
            if (curRule.right.size() == 0) {
                i++;
                continue;
            }

            Symbol firstElemRight = curRule.right.get(0);

            if (!Objects.equals(curRule.left, leftNonTerminal) ||
                    !Objects.equals(firstElemRight.name, rightNonTerminal)) {
                i++;
                continue;
            }

            Rule updRule = ruleList.remove(i);
            updRule.right.remove(0);

            int j = 0;
            while (j < ruleList.size()) {
                if (!Objects.equals(ruleList.get(j).left, rightNonTerminal)) {
                    j++;
                    continue;
                }

                ArrayList<Symbol> addElementList = new ArrayList<>(ruleList.get(j).right);
                addElementList.addAll(updRule.right);

                ruleList.add(Rule.create(updRule.left, addElementList));

                j++;
            }

            i++;
        }
    }

    private void deleteRecursion(List<Rule> ruleList, String nonTerminal) throws Exception {
        ArrayList<ArrayList<Symbol>> alphaArr = new ArrayList<>();
        ArrayList<ArrayList<Symbol>> betaArr = new ArrayList<>();

        for (Rule rule : ruleList) {
            if (!Objects.equals(rule.left, nonTerminal))
                continue;

            Symbol firstElemRight = rule.right.get(0);
            ArrayList<Symbol> temp = new ArrayList<>(rule.right);
            temp.add(new Symbol()
                    .setName(nonTerminal + "'"));
            if (Objects.equals(firstElemRight.name, nonTerminal)) {
                temp.remove(0);
                alphaArr.add(temp);
            }
            else {
                betaArr.add(temp);
            }
        }

        if (alphaArr.size() == 0)
            return;
        if (betaArr.size() == 0) {
            throw new Exception("Недопустимая грамматика");
        }

        updateRules(nonTerminal, ruleList, alphaArr, betaArr);
    }

    private void updateRules(String nonTerminal, List<Rule> ruleList, ArrayList<ArrayList<Symbol>> alphaArr,
                             ArrayList<ArrayList<Symbol>> betaArr) {
        deleteRules(nonTerminal, ruleList);
        updateAlphaRules(nonTerminal, ruleList, alphaArr);
        updateBetaRules(nonTerminal, ruleList, betaArr);
    }

    private void updateAlphaRules(String nonTerminal, List<Rule> ruleList, ArrayList<ArrayList<Symbol>> alphaArr) {
        String newName = nonTerminal + "'";
        for (ArrayList<Symbol> elem : alphaArr) {
            Rule newRule = Rule.create(newName, elem);

            ruleList.add(newRule);
        }

        Rule defRule = Rule.create(newName, new ArrayList<>() { {
            add(new Symbol().setName("ε"));
        }});

        ruleList.add(defRule);
    }

    private void updateBetaRules(String nonTerminal, List<Rule> ruleList, ArrayList<ArrayList<Symbol>> betaArr) {
         for (ArrayList<Symbol> elem : betaArr)
            ruleList.add(Rule.create(nonTerminal, elem));
    }

    private void deleteRules(String nonTerminal, List<Rule> ruleList) {
        int i = 0;
        while (i < ruleList.size()) {
            if (!Objects.equals(ruleList.get(i).left, nonTerminal)) {
                i++;
                continue;
            }

            ruleList.remove(ruleList.get(i));
        }
    }
}
