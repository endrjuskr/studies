__author__ = 'andrzejskrodzki'
# module: tokrules.py
# This module just contains the lexing rules 

from LatteExceptions import LexerException

# Reserved words
reserved = (
    'IF',
    'ELSE',
    'WHILE',
    'RETURN',
    'INT',
    'STRING',
    'BOOLEAN',
    'VOID',
    'TRUE',
    'FALSE')


# Token names.
tokens = reserved + (
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'EQUALS',
    'PLUSPLUS', 'MINUSMINUS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMI',
    'NUMBER', 'SENTENCE', 'ID')


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|\|'
t_AND = r'&&'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_NOT = r'!'
t_EQUALS = r'='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMI = r';'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

# String literal
t_SENTENCE = r'\"([^\\\n]|(\\.))*?\"'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_map.get(t.value, 'ID')    # Check for reserved words
    return t


def t_comment(t):
    r'\#.*|//.*|/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# Define a rule so we can track line numbers 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule 
def t_error(t):
    raise LexerException("Illegal character '%s'" % t.value[0], t.lexer.lineno)