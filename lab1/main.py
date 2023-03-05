from automat.DFA import DFA
from preprocessing.RegexParser import RegexParser


def main():
    #regexStr = input("Введите регулярное выражение: ")
    regex = "(a|b)*"
    data = "aaaabc"
    RegexParser().parseExpression(regex)
    dfa = DFA.createMinDFA(regex)

    dfa.accept(data)


if __name__ == '__main__':
    main()