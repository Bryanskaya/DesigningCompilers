package bmstu.lab.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;

public class Rule {
    @JsonProperty("lhs")
    public String left;

    @JsonProperty("rhs")
    public ArrayList<Symbol> right;

    public static Rule create(String left, ArrayList<Symbol> right) {
        Rule rule = new Rule();
        rule.left = left;
        rule.right = right;
        return rule;
    }
}
