__author__ = 'Andrzej Skrodzki - as292510'

from .LatteParsers.LatteTypes import *
from .LatteParsers.LatteExpressions import *
from .LatteParsers.LatteParameters import *
from .LatteParsers.LatteStatements import *
from .LatteParsers.LatteTopDefinitions import *
from .LatteExceptions import *
import ply.yacc as yacc

from tokrules import tokens

exception_list = []

precedence = (
    ('nonassoc', 'GE', 'GT', 'LE', 'LT', 'NE'),
    ('right', 'AND', 'OR'),
    ('nonassoc', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'PLUSPLUS', 'MINUSMINUS'),
    ('right', 'UNOT', 'UMINUS'),
)


# Program definition


def p_program(p):
    'program : listtopdef'
    p[0] = Program(p[1])

# List definitions


def p_list_expr(p):
    '''listexpr :
            | expr
            | listexpr COMMA expr'''

    if len(p) == 1:
        # empty list
        p[0] = []
    elif len(p) == 2:
        # last expression
        p[0] = [p[1]]
    else:
        # list of expressions
        p[0] = p[1]
        p[0].append(p[3])


def p_list_topdef(p):
    '''listtopdef :
            | topdef
            | listtopdef topdef'''

    if len(p) == 1:
        # empty list
        p[0] = []

    elif len(p) == 2:
        # last function definition
        p[0] = [p[1]]
    else:
        # list of function definitions
        p[0] = p[1]
        p[0].append(p[2])


def p_list_stmt(p):
    '''liststmt : stmt
            | liststmt stmt'''

    if len(p) == 2:
        # last statement
        p[0] = [p[1]]
    else:
        # list of statements
        p[0] = p[1]
        p[0].append(p[2])

def p_list_fields(p):
    '''listfields :
            | field
            | listfields field'''

    if len(p) == 1:
        # empty list
        p[0] = []
    elif len(p) == 2:
        # last statement
        p[0] = [p[1]]
    else:
        # list of statements
        p[0] = p[1]
        p[0].append(p[2])


def p_list_item(p):
    '''listitem : item
            | listitem COMMA item'''

    if len(p) == 1:
        # empty list
        p[0] = []
    elif len(p) == 2:
        # last item
        p[0] = [p[1]]
    else:
        # list of items
        p[0] = p[1]
        p[0].append(p[3])


def p_list_arg(p):
    '''listarg :
            | arg
            | listarg COMMA arg'''

    if len(p) == 1:
        # empty list
        p[0] = []
    elif len(p) == 2:
        # last argument
        p[0] = [p[1]]
    else:
        #list of arguments
        p[0] = p[1]
        p[0].append(p[3])

# Item productions


def p_item_noinit(p):
    'item : ID'
    p[0] = NoInitItem(p[1], p.lineno(1), p.lexpos(1))


def p_item_init(p):
    'item : ID EQUALS expr'
    p[0] = InitItem(p[1], p[3], p.lineno(1), p.lexpos(1))


# Argument definition


def p_arg(p):
    'arg : type ID'
    p[0] = Arg(p[1], p[2], p.lineno(2), p.lexpos(2))


def p_field_s(p):
    'field : type ID SEMI'
    p[0] = Field(p[1], p[2], p.lineno(2), p.lexpos(2))


# Function definition


def p_class_extends(p):
    '''ext :
            | EXTENDS ID'''
    if len(p) == 1:
        p[0] = []

    elif len(p) == 2:
        p[0] = [p[1]]


def p_classdef(p):
    'topdef : CLASS ID ext LBRACE listfields listtopdef RBRACE'
    p[0] = ClassDef(p[2], p[3], p[5], p[6], p.lineno(2))


def p_fndef(p):
    'topdef : type ID LPAREN listarg RPAREN block'
    p[0] = FnDef(p[1], p[2], p[4], p[6], p.lineno(2))


def p_block(p):
    '''block : LBRACE RBRACE
            | LBRACE liststmt RBRACE'''
    if len(p) == 3:
        p[0] = Block([])
    else:
        p[0] = Block(p[2])

# Statement definitions


def p_statement_empty(p):
    'stmt : SEMI'
    p[0] = EmptyStmt(p.lineno(1), p.lexpos(1))


def p_statement_block(p):
    'stmt : block'
    p[0] = BStmt(p[1], p.lineno(1))


def p_statement_decl(p):
    'stmt : type listitem SEMI'
    p[0] = DeclStmt(p[1], p[2], p.lineno(3), p.lexpos(3))


def p_statement_var_ass(p):
    '''stmt : expr EQUALS expr SEMI '''
    p[0] = VarAssStmt(p[1], p[3], p.lineno(2), p.lexpos(2))


def p_statement_incr(p):
    'stmt : expr PLUSPLUS SEMI'
    p[0] = IncrStmt(p[1], p.lineno(2), p.lexpos(2))


def p_statement_decr(p):
    'stmt : expr MINUSMINUS SEMI'
    p[0] = DecrStmt(p[1], p.lineno(2), p.lexpos(2))


def p_statement_ret(p):
    'stmt : RETURN expr SEMI'
    p[0] = RetStmt(p[2], p.lineno(1), p.lexpos(1))


def p_statement_vret(p):
    'stmt : RETURN SEMI'
    p[0] = VRetStmt(p.lineno(1), p.lexpos(1))


def p_statement_cond(p):
    'stmt : IF LPAREN expr RPAREN stmt'
    p[0] = CondStmt(p[3], p[5], p.lineno(1), p.lexpos(1))


def p_statement_condelse(p):
    'stmt : IF LPAREN expr RPAREN stmt ELSE stmt'
    p[0] = CondElseStmt(p[3], p[5], p[7], p.lineno(1), p.lexpos(1))


def p_statement_while(p):
    'stmt : WHILE LPAREN expr RPAREN stmt'
    p[0] = WhileStmt(p[3], p[5], p.lineno(1), p.lexpos(1))


def p_statement_sexp(p):
    'stmt : expr SEMI'
    p[0] = SExpStmt(p[1], p.lineno(2), p.lexpos(2))

def p_statement_for(p):
    'stmt : FOR LPAREN type_s ID COL expr RPAREN stmt'
    p[0] = ForStmt(p[4], p[3], p[6], p[8], p.lineno(1), p.lexpos(1))


# Expression definitions

def p_expression_array_init(p):
    'expr6 : NEW type_s LARRAY expr RARRAY'
    p[0] = EArrayInit(p[2], p[4], p.lineno(1), p.lexpos(1))


def p_expression_object_init(p):
    'expr6 : NEW ID'
    p[0] = EObjectInit(Type(p[2]), p.lineno(1), p.lexpos(1))


def p_expression_var(p):
    'expr6 : ID'
    p[0] = EVar(p[1], p.lineno(1), p.lexpos(1))


def p_expression_field(p):
    'expr6 : expr6 DOT ID'
    p[0] = EObjectField(p[1], p[3], p.lineno(1), p.lexpos(1))


def p_expression_array(p):
    'expr6 : expr6 LARRAY expr RARRAY'
    p[0] = EArrayApp(p[1], p[3], p.lineno(1), p.lexpos(1))


def p_expression_int(p):
    'expr6 : NUMBER'
    p[0] = ELitInt(p[1], p.lineno(1), p.lexpos(1))


def p_expression_null(p):
    '''expr6 : LPAREN ID RPAREN NULL '''
    p[0] = ELitNull(p[2], p.lineno(1), p.lexpos(1))


def p_expression_boolean(p):
    '''expr6 : TRUE
            | FALSE'''
    p[0] = ELitBoolean(p[1], p.lineno(1), p.lexpos(1))


def p_expression_app(p):
    'expr6 : ID LPAREN listexpr RPAREN'
    p[0] = EApp(p[1], p[3], p.lineno(2), p.lexpos(2))


def p_expression_method_app(p):
    'expr6 : expr6 DOT ID LPAREN listexpr RPAREN'
    p[0] = EMethodApp(p[1], p[3], p[5], p.lineno(2), p.lexpos(2))


def p_expression_group(p):
    'expr6 : LPAREN expr RPAREN'
    p[0] = p[2]


def p_expression_string(p):
    'expr6 : SENTENCE'
    p[0] = EString(p[1], p.lineno(1), p.lexpos(1))


def p_expression_neg(p):
    'expr5 : MINUS expr6  %prec UMINUS'
    p[0] = ENeg(p[2], p.lineno(1), p.lexpos(1))


def p_expression_not_1(p):
    '''expr5 : expr6'''
    p[0] = p[1]


def p_expression_not_2(p):
    '''expr5 : NOT expr6 %prec UNOT'''
    p[0] = ENot(p[2], p.lineno(1), p.lexpos(1))


def p_expression_mul_1(p):
    '''expr4 : expr5'''
    p[0] = p[1]


def p_mulop(p):
    '''mulop : TIMES
            | DIVIDE
            | MOD'''
    p[0] = p[1]


def p_expression_mul_2(p):
    '''expr4 : expr4 mulop expr5'''
    p[0] = EMul(p[1], p[3], p[2], p[1].no_line, p[1].pos + 1)


def p_addop(p):
    '''addop : PLUS
            | MINUS'''
    p[0] = p[1]


def p_expression_add_1(p):
    '''expr3 : expr3 addop expr4'''
    p[0] = EAdd(p[1], p[3], p[2], p[1].no_line, p[1].pos + 1)


def p_expression_add_3(p):
    '''expr3 : expr4'''
    p[0] = p[1]


def p_relop(p):
    '''relop : LT
            | LE
            | GT
            | GE
            | EQ
            | NE'''
    p[0] = p[1]


def p_expression_rel_1(p):
    '''expr2 : expr2 relop expr3'''
    p[0] = ERel(p[1], p[3], p[2], p[1].no_line, p[1].pos + 1)


def p_expression_rel_2(p):
    '''expr2 : expr3'''
    p[0] = p[1]


def p_expression_and_1(p):
    '''expr1 : expr2 AND expr1'''
    p[0] = EAnd(p[1], p[3], p.lineno(2), p.lexpos(2))


def p_expression_and_2(p):
    '''expr1 : expr2'''
    p[0] = p[1]


def p_expression_or_1(p):
    '''expr : expr1 OR expr'''
    p[0] = EOr(p[1], p[3], p.lineno(2), p.lexpos(2))


def p_expression_or_2(p):
    '''expr : expr1'''
    p[0] = p[1]

# Type definition

def p_type_s(p):
    '''type_s : INT
            | STRING
            | VOID
            | BOOLEAN '''
    p[0] = Type(p[1])

def p_type_1(p):
    '''type : type_s'''
    p[0] = p[1]

def p_type_a(p):
    '''type : type_s LARRAY RARRAY'''
    p[0] = ArrayType(p[1])

# Error definition


def p_error(p):
    if p is None:
        return
    exception_list.append(SyntaxException("Wrong expression '" + str(p.value) + "'.", p.lineno, pos=p.lexpos))
    tok = None
    while 1:
        tok = yacc.token()
        if not tok:
            break
        if tok.type == 'SEMI':
            tok = yacc.token()
    yacc.errok()
    return tok


def get_parser():
    return yacc.yacc(write_tables=0, debug=0, outputdir="src")