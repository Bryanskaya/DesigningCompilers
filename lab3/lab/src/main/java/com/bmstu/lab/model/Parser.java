package com.bmstu.lab.model;

import com.bmstu.lab.exception.ParserException;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;

@Slf4j
public class Parser {
    protected HashMap<String, String> first = new HashMap<>() {{
        put("expression", "iC(");
        put("arith_expression", "iC(");
        put("arith_expression_stroke", "+-e");
        put("arith_expression_brackets", "(");
        put("term", "iC(");
        put("factor", "iC(");
        put("identifier", "i");
        put("constant", "C");
        put("term_stroke", "+/e");
        put("op_relationship", "<=>");
        put("op_sum", "+-");
        put("op_mult", "*/");
    }};

    private int i = 0;
    private String s = null;

    public void run() {
        expression();
    }

    public boolean eval(String str) {
        i = 0;
        s = str;

        boolean res = false;
        try {
            run();
            res = i == s.length();
        } catch (Exception e) {
            log.error(e.getMessage());
        }

        return res;
    }

    protected boolean inFirst(String elem) {
        if (i >= s.length())
            return false;

        String curSymbol = Character.toString(s.charAt(i));

        return first.get(elem).contains(curSymbol);
    }

    protected void subStrStartWithTerm(String ... items) {
        for (String item: items)
            if (s.substring(i).startsWith(item)) {
                i += item.length();
                return;
            }
        throw new ParserException(String.format("Unexpected symbol in input string, position=%d", i));
    }

    protected void expression() {
        if (inFirst("arith_expression")) {
            arithExpression();
            if (inFirst("op_relationship")) {
                opRelationship();
                arithExpression();
            }
        }
        else
            throw new ParserException(String.format("Unexpected symbol in input string, position=%d", i));
    }

    private void arithExpression() {
        term();
        arithExpressionStroke();
    }

    private void arithExpressionStroke() {
        if (inFirst("op_sum")) {
            opSum();
            term();
            arithExpressionStroke();
        }
    }

    private void term() {
        factor();
        termStroke();
    }

    private void termStroke() {
        if (inFirst("op_mult")) {
            opMult();
            factor();
            termStroke();
        }
    }

    private void factor() {
        if (inFirst("identifier"))
            identifier();
        else if (inFirst("constant"))
            constant();
        else if (inFirst("arith_expression_brackets"))
            arithExpressionBrackets();
        else
            throw new ParserException(String.format("Unexpected symbol in input string, position=%d", i));
    }

    private void arithExpressionBrackets() {
        subStrStartWithTerm("(");
        arithExpression();
        subStrStartWithTerm(")");
    }

    private void opRelationship() {
        subStrStartWithTerm("<>", "<=", ">=", "<", "=", ">");
    }

    private void opSum() {
        subStrStartWithTerm("+", "-");
    }

    private void opMult() {
        subStrStartWithTerm("*", "/");
    }

    protected void identifier() {
        subStrStartWithTerm("i");
    }

    private void constant() {
        subStrStartWithTerm("C");
    }
}
