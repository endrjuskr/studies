__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.Statements.IncrStmt import *
from LatteParsers.Statements.DeclStmt import *
from LatteParsers.Statements.DecrStmt import *
from LatteParsers.Statements.CondStmt import *
from LatteParsers.Statements.CondElseStmt import *
from LatteParsers.Statements.AssStmt import *
from LatteParsers.Statements.EmptyStmt import *
from LatteParsers.Statements.BStmt import *
from LatteParsers.Statements.RetStmt import *
from LatteParsers.Statements.SExpStmt import *
from LatteParsers.Statements.VRetStmt import *
from LatteParsers.Statements.WhileStmt import *
from LatteParsers.Programs.Block import *
from LatteParsers.Programs.Program import *
from LatteParsers.Parameters.Arg import *
from LatteParsers.Parameters.InitItem import *
from LatteParsers.Parameters.NoInitItem import *
from LatteParsers.Expressions.EAdd import *
from LatteParsers.Expressions.EAnd import *
from LatteParsers.Expressions.EApp import *
from LatteParsers.Expressions.ENeg import *
from LatteParsers.Expressions.ENot import *
from LatteParsers.Expressions.EMul import *
from LatteParsers.Expressions.ERel import *
from LatteParsers.Expressions.ELitInt import *
from LatteParsers.Expressions.ELitBoolean import *
from LatteParsers.Expressions.EString import *
from LatteParsers.Expressions.EVar import *
from LatteParsers.Expressions.EOr import *
import ply.yacc as yacc

from tokrules import tokens

precedence = (
    ('nonassoc', 'GE', 'GT', 'LE', 'LT', 'EQ', 'NE'),
    ('right', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'PLUSPLUS', 'MINUSMINUS'),
    ('right', 'UMINUS'),
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
    '''listtopdef : topdef
            | listtopdef topdef'''

    if len(p) == 2:
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


def p_list_item(p):
    '''listitem :
            | item
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

# Function definition


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


def p_statement_ass(p):
    'stmt : ID EQUALS expr SEMI'
    p[0] = AssStmt(p[1], p[3], p.lineno(1), p.lexpos(1))


def p_statement_incr(p):
    'stmt : ID PLUSPLUS SEMI'
    p[0] = IncrStmt(p[1], p.lineno(1), p.lexpos(1))


def p_statement_decr(p):
    'stmt : ID MINUSMINUS SEMI'
    p[0] = DecrStmt(p[1], p.lineno(1), p.lexpos(1))


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
    p[0] = SExpStmt(p[1], p.lineno(1), p.lexpos(1))

# Expression definitions


def p_expression_var(p):
    'expr6 : ID'
    p[0] = EVar(p[1], p.lineno(1), p.lexpos(1))


def p_expression_int(p):
    'expr6 : NUMBER'
    p[0] = ELitInt(p[1], p.lineno(1), p.lexpos(1))


def p_expression_boolean(p):
    '''expr6 : TRUE
            | FALSE'''
    p[0] = ELitBoolean(p[1], p.lineno(1), p.lexpos(1))


def p_expression_app(p):
    'expr6 : ID LPAREN listexpr RPAREN'
    p[0] = EApp(p[1], p[3], p.lineno(1), p.lexpos(1))


def p_expression_group(p):
    'expr6 : LPAREN expr RPAREN'
    p[0] = p[2]


def p_expression_string(p):
    'expr6 : SENTENCE'
    p[0] = EString(p[1], p.lineno(1), p.lexpos(1))


def p_expression_neg(p):
    'expr5 : MINUS expr6  %prec UMINUS'
    p[0] = ENeg(p[2], p.lineno(1), p.lexpos(2))


def p_expression_not_1(p):
    '''expr5 : expr6'''
    p[0] = p[1]


def p_expression_not_2(p):
    '''expr5 : NOT expr6'''
    p[0] = ENot(p[2], p.lineno(1), p.lexpos(2))


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
    p[0] = EMul(p[1], p[3], p[2], p[1].no_line, p[1].pos)


def p_addop(p):
    '''addop : PLUS
            | MINUS'''
    p[0] = p[1]


def p_expression_add_1(p):
    '''expr3 : expr3 addop expr4'''
    p[0] = EAdd(p[1], p[3], p[2], p[1].no_line, p[1].pos)


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
    p[0] = ERel(p[1], p[3], p[2], p[1].no_line, p[1].pos)


def p_expression_rel_2(p):
    '''expr2 : expr3'''
    p[0] = p[1]


def p_expression_and_1(p):
    '''expr1 : expr2 AND expr1'''
    p[0] = EAnd(p[1], p[3], p[1].no_line, p[1].pos)


def p_expression_and_2(p):
    '''expr1 : expr2'''
    p[0] = p[1]


def p_expression_or_1(p):
    '''expr : expr1 OR expr'''
    p[0] = EOr(p[1], p[3], p[1].no_line, p[1].pos)


def p_expression_or_2(p):
    '''expr : expr1'''
    p[0] = p[1]

# Type definition


def p_type(p):
    '''type : INT
            | STRING
            | VOID
            | BOOLEAN'''
    p[0] = Type.Type(p[1])

# Error definition


def p_error(p):
    raise SyntaxException.SyntaxException("Wrong expression '" + p.value + "'.", p.lineno, pos=p.lexpos)


def get_parser():
    return yacc.yacc(write_tables=0, debug=0)