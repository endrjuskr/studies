__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class SExpStmt(StmtBase):
    def __init__(self, expr, no_line, pos):
        super(SExpStmt, self).__init__("sexpstmt", no_line, pos)
        self.expr = expr

    def type_check(self, env):
        # Here we assume that the only expression is invocation of void function.
        self.expr.type_check(env, expected_type=Type.Type("void"))