__author__ = 'andrzejskrodzki'
# ------------------------------------------------------------
# lattelex.py
#
# tokenizer for a Latte language
# ------------------------------------------------------------

import ply.lex as lex

import tokrules


def get_lexer():
    return lex.lex(module=tokrules)