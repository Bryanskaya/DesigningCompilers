package bmstu.lab.Services;

import bmstu.lab.Entities.GrammarInfo;
import bmstu.lab.Entities.Rule;
import bmstu.lab.Entities.Symbol;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Objects;

public class UnreachableSymbolsService {
    public void delete(GrammarInfo grammarInfo) {
        HashSet<String> vPrev = new HashSet<>();
        HashSet<String> vCurr = new HashSet<>();

        vPrev.add(grammarInfo.startSymbol);

        while (true) {
            for (Rule rule : grammarInfo.productions) {
                if (!vPrev.contains(rule.left))
                    continue;

                for (Symbol elem : rule.right)
                    vCurr.add(elem.name);
            }

            vCurr.addAll(vPrev);

            if (vPrev.equals(vCurr))
                break;

            vPrev = new HashSet<>(vCurr);
            vCurr.clear();
        }

        update(grammarInfo, vCurr);
    }

    private void update(GrammarInfo grammarInfo, HashSet<String> v) {
        updateNonTerminalSymbols(grammarInfo, v);
        updateTerminalSymbols(grammarInfo, v);
        updateRules(grammarInfo, v);
    }

    private void updateNonTerminalSymbols(GrammarInfo grammarInfo, HashSet<String> v) {
        grammarInfo.nonTerminalSymbols.retainAll(v);
    }

    private void updateTerminalSymbols(GrammarInfo grammarInfo, HashSet<String> v) {
        ArrayList<Symbol> termList = new ArrayList<>();
        for (Symbol term : grammarInfo.terminalSymbols)
            if (v.contains(term.spell))
                termList.add(term);

        grammarInfo.terminalSymbols = termList;
    }

    private void updateRules(GrammarInfo grammarInfo, HashSet<String> v) {
        ArrayList<Rule> ruleList = new ArrayList<>();
        for (Rule rule : grammarInfo.productions) {
            if (!grammarInfo.isTerminalElement(rule.left) && !v.contains(rule.left))
                continue;

            int cnt = 0;
            for (Symbol elemRight : rule.right)
                if (v.contains(elemRight.name) || Objects.equals(elemRight.name, "ε"))
                    cnt++;

            if (cnt == rule.right.size())
                ruleList.add(rule);
        }

        grammarInfo.productions = ruleList;
    }
}
