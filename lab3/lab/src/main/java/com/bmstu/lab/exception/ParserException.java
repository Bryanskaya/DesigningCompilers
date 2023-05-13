package com.bmstu.lab.exception;

public class ParserException extends RuntimeException {
    public static String MSG = "PARSER: error was caught, err=%s.";

    public ParserException(String err) {
        super(String.format(MSG, err));
    }
}
