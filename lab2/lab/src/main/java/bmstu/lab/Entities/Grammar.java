package bmstu.lab.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;

import java.util.*;

@Slf4j
@Accessors(chain = true)
@Getter
@Setter
public class Grammar {
    @JsonProperty("grammar")
    public GrammarInfo grammarInfo;

    public void print() {
        printName();
        printStartSymbol();
        printNonTerminal();
        printTerminal();
        printRule();
        log.info("-----------------------");
    }

    private void printName() {
        log.info("Name: {}", grammarInfo.name);
    }

    private void printStartSymbol() {
        log.info("Start symbol: {}", grammarInfo.startSymbol);
    }

    private void printNonTerminal() {
        log.info("Nonterminal symbols: {}", String.join(", ", grammarInfo.nonTerminalSymbols));
    }

    private void printTerminal() {
        ArrayList<String> termList = new ArrayList<>();
        for (Symbol elem : grammarInfo.terminalSymbols)
            termList.add(elem.spell);
        log.info("Terminal symbols: {}", String.join(", ", termList));
    }

    private void printRule() {
        log.info("Rules:");
        HashMap<String, ArrayList<String>> resRules = new HashMap<>();
        for (Rule rule : grammarInfo.productions) {
            if (!resRules.containsKey(rule.left))
                resRules.put(rule.left, new ArrayList<>());

            StringBuilder ruleStr = new StringBuilder();
            for (Symbol elem : rule.right)
                ruleStr.append(elem.name);

            resRules.get(rule.left).add(ruleStr.toString());
        }

        for (Map.Entry<String, ArrayList<String>> set : resRules.entrySet())
            log.info("{} -> {}", set.getKey(), String.join(" | ", resRules.get(set.getKey())));
    }

    public boolean isEqual(Grammar o) {
        GrammarInfo cmpGrammar = o.getGrammarInfo();

        return grammarInfo.isEqualName(cmpGrammar.getName()) &&
                grammarInfo.isEqualStartSymbol(cmpGrammar.getStartSymbol()) &&
                grammarInfo.isEqualTerminalSymbols(cmpGrammar.getTerminalSymbols()) &&
                grammarInfo.isEqualNonTerminalSymbols(cmpGrammar.getNonTerminalSymbols()) &&
                grammarInfo.isEqualProductions(cmpGrammar.getProductions());
    }
}
