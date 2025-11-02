import sys
from lark import Lark, tree, exceptions as exLark

WEAK_CONSTRAINT = 'weak_constraint'

VARIABLE = 'variable'

STATEMENT = 'statement'

FACT = 'fact'

DISJUNCTION = 'disjunction'

CONSTRAINT_RULE = 'constraint_rule'

CLASSICAL_RULE = 'classical_rule'

AGGREGATE_FUNCTION = 'aggregate_function'

parser = Lark(r'''
s : program | "^" 

program : statements
|         query
|         statements query

statements : statements statement
|            statement

classical_rule: head CONS body DOT

constraint_rule: CONS body DOT | CONS DOT

fact: head DOT

weak_constraint: WCONS body DOT SQUARE_OPEN weight_at_level SQUARE_CLOSE
          | WCONS DOT SQUARE_OPEN weight_at_level SQUARE_CLOSE

statement : constraint_rule
          | head CONS DOT
          | classical_rule
          | fact
          | weak_constraint
          | optimize DOT

query : classical_literal QUERY_MARK

head : disjunction | choice | simplehead

body : naf_literal
|      aggregate
|      NAF aggregate
|      body COMMA naf_literal
|      body COMMA aggregate
|      body COMMA NAF aggregate

simplehead: classical_literal

disjunction : disjunction OR classical_literal

choice : CURLY_OPEN choice_elements CURLY_CLOSE binop term
|        CURLY_OPEN CURLY_CLOSE binop term
|        CURLY_OPEN CURLY_CLOSE
|        CURLY_OPEN choice_elements CURLY_CLOSE
|        term binop CURLY_OPEN choice_elements CURLY_CLOSE
|        term binop CURLY_OPEN CURLY_CLOSE binop term
|        term binop CURLY_OPEN CURLY_CLOSE
|        term binop CURLY_OPEN choice_elements CURLY_CLOSE binop term
|	     CURLY_OPEN choice_elements CURLY_CLOSE binop classical_literal
|        CURLY_OPEN CURLY_CLOSE binop classical_literal
|        classical_literal binop CURLY_OPEN choice_elements CURLY_CLOSE
|        classical_literal binop CURLY_OPEN CURLY_CLOSE binop classical_literal
|        classical_literal binop CURLY_OPEN CURLY_CLOSE binop term
|        term binop CURLY_OPEN CURLY_CLOSE binop classical_literal
|        classical_literal binop CURLY_OPEN CURLY_CLOSE
|        classical_literal binop CURLY_OPEN choice_elements CURLY_CLOSE binop classical_literal
|        classical_literal binop CURLY_OPEN choice_elements CURLY_CLOSE binop term
|        term binop CURLY_OPEN choice_elements CURLY_CLOSE binop classical_literal

choice_elements : choice_elements SEMICOLON choice_element
|                 choice_element

choice_element : classical_literal COLON naf_literal
|               classical_literal COLON
|               classical_literal

aggregate : aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE binop term
|           aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE binop classical_literal
|           aggregate_function CURLY_OPEN CURLY_CLOSE binop term
|           aggregate_function CURLY_OPEN CURLY_CLOSE binop classical_literal
|           aggregate_function CURLY_OPEN CURLY_CLOSE
|           aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE
|           b aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE
|           b aggregate_function CURLY_OPEN CURLY_CLOSE binop term
|           b aggregate_function CURLY_OPEN CURLY_CLOSE binop classical_literal
|           b aggregate_function CURLY_OPEN CURLY_CLOSE
|           b aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE binop term
|           b aggregate_function CURLY_OPEN aggregate_elements CURLY_CLOSE binop classical_literal

aggregate_elements : aggregate_elements SEMICOLON aggregate_element
|                    aggregate_element

aggregate_element : terms COLON naf_literals
|                   terms
|                   terms COLON
|                   COLON
|                   COLON naf_literals

aggregate_function : AGGREGATE_COUNT | AGGREGATE_MAX | AGGREGATE_MIN | AGGREGATE_SUM

optimize : optimize_function CURLY_OPEN optimize_elements CURLY_CLOSE
|          optimize_function CURLY_OPEN CURLY_CLOSE

optimize_function : MAXIMIZE | MINIMIZE

optimize_elements : optimize_elements SEMICOLON optimize_element 
|                   optimize_element

optimize_element : weight_at_level COLON naf_literals
|                  weight_at_level COLON
|                  weight_at_level

weight_at_level : term AT term COMMA terms
|                 classical_literal AT term COMMA terms
|                 term AT classical_literal COMMA terms
|                 classical_literal AT classical_literal COMMA terms
|                 term AT term
|                 classical_literal AT term
|                 term AT classical_literal
|                 classical_literal AT classical_literal
|                 term
|                 classical_literal

naf_literals : naf_literals COMMA naf_literal 
|              naf_literal

naf_literal : classical_literal
|             NAF classical_literal
|             builtin_atom


builtin_atom : b term | b classical_literal

binop : EQUAL | UNEQUAL | LESS | GREATER | LESS_OR_EQ | GREATER_OR_EQ

terms : terms COMMA term 
|       terms COMMA classical_literal
|       term
|       classical_literal

variable: VARIABLE
|      ANONYMOUS_VARIABLE

term : NUMBER
|      STRING
|      variable
|      PAREN_OPEN term PAREN_CLOSE
|      termdue term
|      termdue termdue

termdue: NUMBER arithop
|      STRING arithop
|      VARIABLE arithop
|      ANONYMOUS_VARIABLE arithop
|      PAREN_OPEN termdue PAREN_CLOSE arithop
|      PAREN_OPEN term PAREN_CLOSE arithop
|      ID PAREN_OPEN terms PAREN_CLOSE arithop

arithop : PLUS | MINUS | TIMES | DIV

classical_literal : ID
|   ID PAREN_OPEN PAREN_CLOSE
|   ID PAREN_OPEN terms PAREN_CLOSE
|      MINUS classical_literal



b: term binop
|   classical_literal binop

ID: /[a-z][A-Za-z0-9_]*/
VARIABLE: /[A-Z][A-Za-z0-9_]*/
STRING: "\"" ("\\\""|/[^"]/)* "\""
NUMBER: "0"|/[1-9][0-9]*/
ANONYMOUS_VARIABLE: "_"
DOT: "."
COMMA: ","
QUERY_MARK: "?"
COLON: ":"
SEMICOLON: ";"
OR: "|"
NAF: "not"
CONS: ":-"
WCONS: ":~"
PLUS: "+"
MINUS: "-"
TIMES: "*"
DIV: "/"
AT: "@"
PAREN_OPEN: "("
PAREN_CLOSE: ")"
SQUARE_OPEN: "["
SQUARE_CLOSE: "]"
CURLY_OPEN: "{"
CURLY_CLOSE: "}"
EQUAL: "="
UNEQUAL: "<>"|"!="
LESS: "<"
GREATER: ">"
LESS_OR_EQ: "<="
GREATER_OR_EQ: ">="
AGGREGATE_COUNT: "#count"
AGGREGATE_MAX: "#max"
AGGREGATE_MIN: "#min"
AGGREGATE_SUM: "#sum"
MINIMIZE: "#minimi" /[zs]/ "e"
MAXIMIZE: "#maximi" /[zs]/ "e"
COMMENT: "%" /([^*\n][^\n]*)?\n/
MULTI_LINE_COMMENT: "%*" /([^*]|\*[^%])/* "*%"
BLANK: /[ \t\n]/+

%ignore COMMENT
%ignore MULTI_LINE_COMMENT
%ignore BLANK
''', start="s", parser='lalr', debug=True)


def isCorrectSentence(sentence):
    try:
        parser.parse(sentence)
        return True
    except exLark.UnexpectedToken as e:
        return e


class SentenceParsing:
    def __init__(self, sentence: str):
        self.sentence = sentence
        self.parsedSentence = parser.parse(sentence)


    def make_png(self, filename):
        tree.pydot__tree_to_png(self.parsedSentence, filename)

    def count(self, construct):
        if construct == WEAK_CONSTRAINT:
            return self.weakConstraints()
        if construct == VARIABLE:
            return self.variables()
        if construct == STATEMENT:
            return self.rules()
        if construct == FACT:
            return self.facts()
        if construct == DISJUNCTION:
            return self.disjuntiveRule()
        if construct == CONSTRAINT_RULE:
            return self.constraintRules()
        if construct == CLASSICAL_RULE:
            return self.classicalRule()
        if construct == AGGREGATE_FUNCTION:
            return self.aggregateLiterals()
        return 0

    def countConstruct(self, construct):
        l = (list(self.parsedSentence.find_data(construct)))
        return len(l)

    def aggregateLiterals(self):
        return self.countConstruct(AGGREGATE_FUNCTION)

    def classicalRule(self):
        return self.countConstruct(CLASSICAL_RULE)

    def constraintRules(self):
        return self.countConstruct(CONSTRAINT_RULE)

    def disjuntiveRule(self):
        return self.countConstruct(DISJUNCTION)

    def facts(self):
        return self.countConstruct(FACT)

    def rules(self):
        return self.countConstruct(STATEMENT)

    def variables(self):
        splitSentence = self.sentence.split('.')
        l = []
        for ss in splitSentence:
            if len(ss) > 0:
                ss += '.'
                l.append(parser.parse(ss).find_data(VARIABLE))
        return len(l)

    def weakConstraints(self):
        return self.countConstruct(WEAK_CONSTRAINT)

    def pretty(self):
        return self.parsedSentence.pretty()

    def __repr__(self):
        return self.pretty()

# aggregateLiterals     => aggregate_function
# classicalRule         => classical_rule
# constraintRules       => constraint_rule
# disjuntiveRule        => disjunction
# facts                 => fact
# rules                 => statement
# variables             => variable
# weakConstraints       => weak_constraint


if __name__ == '__main__':
    s2 = 'osoihh. '
    print(isCorrectSentence(s2))
