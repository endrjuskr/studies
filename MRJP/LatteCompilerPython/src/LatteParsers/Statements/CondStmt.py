__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class CondStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(CondStmt, self).__init__("condstmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt


    def type_check(self, env):
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt.type_check(env)

    def return_check(self):
        if self.expr.value is True:
            return self.stmt.return_check()
        else:
            return False