package bmstu.lab.Controllers;

import bmstu.lab.Entities.Grammar;
import bmstu.lab.Entities.GrammarInfo;
import bmstu.lab.Entities.Rule;
import bmstu.lab.Entities.Symbol;
import bmstu.lab.Services.EmptyLanguageService;
import bmstu.lab.Services.RecursionService;
import bmstu.lab.Services.UnreachableSymbolsService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Objects;

@Slf4j
public class GrammarController {
    public static Grammar process(String filenameJson){
        Grammar grammar;

        try{
             grammar = readGrammarFromFile(filenameJson);
        } catch (IOException e){
            log.error("Error in read file action: {}", e.getMessage());
            return null;
        }

        log.info("Init grammar");
        grammar.print();

        try {
            deleteLeftRecursion(grammar.grammarInfo);
        } catch (Exception e) {
            log.error("Error in deleting recursion: {}", e.getMessage());
            return null;
        }

        log.info("After deletion recursion");
        grammar.print();

        return deleteUselessSymbols(grammar);
    }

    public static Grammar processWithoutLeftRecursion(String filenameJson){
        Grammar grammar;

        try{
            grammar = readGrammarFromFile(filenameJson);
        } catch (IOException e){
            log.error("Error in read file action: {}", e.getMessage());
            return null;
        }

        log.info("Init grammar");
        grammar.print();

        return deleteUselessSymbols(grammar);
    }

    private static Grammar deleteUselessSymbols(Grammar grammar) {
        HashSet<String> ne = isEmptyLanguage(grammar.grammarInfo);
        if (ne == null) {
            log.error("Empty language");
            return null;
        }
        log.info("ne: {}", String.join(", ", ne));

        updateGrammar(ne, grammar.grammarInfo);
        log.info("After update");
        grammar.print();

        deleteUnreachableSymbols(grammar.grammarInfo);

        log.info("After deletion unreachable symbols");
        grammar.print();

        //writeGrammarToFile(grammar);
        return grammar;
    }

    public static Grammar readGrammarFromFile(String filenameJson) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(filenameJson), Grammar.class);
    }

    private static void writeGrammarToFile(Grammar grammar) {
        ObjectMapper mapper = new ObjectMapper();
        try {
            mapper.writeValue(new File("src/main/resources/test_res2.json"), grammar);
        } catch (Exception e) {
            log.error("Error while writing to file: {}", e.getMessage());
        }
    }

    private static void deleteLeftRecursion(GrammarInfo grammarInfo) throws Exception {
        new RecursionService().deleteLeftRecursion(grammarInfo);
    }

    private static HashSet<String> isEmptyLanguage(GrammarInfo grammarInfo) {
        return new EmptyLanguageService().isEmpty(grammarInfo);
    }

    private static void updateGrammar(HashSet<String> ne, GrammarInfo grammarInfo) {
        ArrayList<String> neList = new ArrayList<>(ne);
        grammarInfo.nonTerminalSymbols.retainAll(neList);

        ArrayList<Rule> ruleList = new ArrayList<>();
        for (Rule rule : grammarInfo.productions) {
            if (!grammarInfo.isTerminalElement(rule.left) && !ne.contains(rule.left))
                continue;

            int cnt = 0;
            for (Symbol elemRight : rule.right) {
                if (grammarInfo.isTerminalSymbol(elemRight) ||
                        ne.contains(elemRight.name) ||
                        Objects.equals(elemRight.name, "ε"))
                    cnt++;
            }

            if (cnt == rule.right.size())
                ruleList.add(rule);
        }

        grammarInfo.productions = ruleList;
    }

    private static void deleteUnreachableSymbols(GrammarInfo grammarInfo) {
        new UnreachableSymbolsService().delete(grammarInfo);
    }
}
