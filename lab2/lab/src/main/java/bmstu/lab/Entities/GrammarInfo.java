package bmstu.lab.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.experimental.Accessors;

import java.util.*;

@Accessors(chain = true)
@Getter
public class GrammarInfo {

    @JsonProperty("-name")
    public String name;

    @JsonProperty("terminalsymbols")
    public ArrayList<Symbol> terminalSymbols;

    @JsonProperty("nonterminalsymbols")
    public ArrayList<String> nonTerminalSymbols;

    @JsonProperty("productions")
    public ArrayList<Rule> productions;

    @JsonProperty("startsymbol")
    public String startSymbol;


    public boolean isTerminalSymbol(Symbol symbol) {
        for (Symbol term : terminalSymbols)
            if (Objects.equals(term.spell, symbol.name))
                return true;

        return false;
    }

    public boolean isTerminalElement(String elem) {
        for (Symbol term : terminalSymbols)
            if (Objects.equals(term.name, elem))
                return true;
        return false;
    }

    public boolean isEqualName(String name) {
        return Objects.equals(this.getName(), name);
    }

    public boolean isEqualTerminalSymbols(ArrayList<Symbol> terminalSymbols) {
        HashSet<String> curSet = getTerminalsSet(this.getTerminalSymbols());
        HashSet<String> cmpSet = getTerminalsSet(terminalSymbols);

        return curSet.equals(cmpSet);
    }

    private HashSet<String> getTerminalsSet(ArrayList<Symbol> terminalSymbols) {
        HashSet<String> termSet = new HashSet<>();
        terminalSymbols.forEach(term -> termSet.add(term.name));
        return termSet;
    }

    public boolean isEqualStartSymbol(String startSymbol) {
        return Objects.equals(this.getStartSymbol(), startSymbol);
    }

    public boolean isEqualNonTerminalSymbols(ArrayList<String> nonTerminalSymbols) {
        return this.getNonTerminalSymbols().equals(nonTerminalSymbols);
    }

    public boolean isEqualProductions(ArrayList<Rule> ruleList) {
        HashMap<String, ArrayList<String>> curMap = createRuleDict(this.productions);
        HashMap<String, ArrayList<String>> cmpMap = createRuleDict(ruleList);

        return curMap.equals(cmpMap);
    }

    private HashMap<String, ArrayList<String>> createRuleDict(ArrayList<Rule> ruleList) {
        HashMap<String, ArrayList<String>> ruleDict = new HashMap<>();

        ruleList.forEach(rule -> {
            if (!ruleDict.containsKey(rule.left))
                ruleDict.put(rule.left, new ArrayList<>());

            StringBuilder sBuilder = new StringBuilder();
            rule.right.forEach(elem -> sBuilder.append(elem.name));
            ruleDict.get(rule.left).add(sBuilder.toString());
        });

        return ruleDict;
    }
}
