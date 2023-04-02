package bmstu.lab.Services;

import bmstu.lab.Entities.GrammarInfo;
import bmstu.lab.Entities.Rule;
import bmstu.lab.Entities.Symbol;
import com.fasterxml.jackson.databind.JsonSerializer;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Objects;

public class EmptyLanguageService {
    public HashSet<String> isEmpty(GrammarInfo grammarInfo) {
        HashSet<String> cPrev = new HashSet<>();
        HashSet<String> cCurr = new HashSet<>();

        while (true) {
            for (Rule rule : grammarInfo.productions) {
                if (isFitCondition(rule.right, cPrev, grammarInfo))
                    cCurr.add(rule.left);
            }

            cCurr.addAll(cPrev);

            if (cPrev.equals(cCurr))
                break;

            cPrev = new HashSet<>(cCurr);
            cCurr.clear();
        }

        return (cCurr.contains(grammarInfo.startSymbol)) ? cCurr : null;
    }

    private boolean isFitCondition(ArrayList<Symbol> ruleRight, HashSet<String> cPrev, GrammarInfo grammarInfo) {
        for (Symbol elem : ruleRight) {
            if (grammarInfo.isTerminalSymbol(elem) || cPrev.contains(elem.name) || Objects.equals(elem.name, "ε"))
                continue;
            return false;
        }

        return true;
    }
}
