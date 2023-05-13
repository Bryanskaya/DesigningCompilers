package com.bmstu.lab.model;

public class CParser extends Parser{
    public CParser() {
        first.put("tail_not_empty", ";");

    }

    public void run() {
        program();
    }

    private void program() {
        block();
    }

    private void block() {
        subStrStartWithTerm("{");
        listParams();
        subStrStartWithTerm("}");
    }

    private void listParams() {
        operator();
        tail();
    }

    private void tail() {
        if (inFirst("tail_not_empty"))
            tail_notEmpty();
    }

    private void tail_notEmpty() {
        subStrStartWithTerm(";");
        operator();
        tail();
    }

    private void operator() {
        identifier();
        subStrStartWithTerm("=");
        expression();
    }
}
