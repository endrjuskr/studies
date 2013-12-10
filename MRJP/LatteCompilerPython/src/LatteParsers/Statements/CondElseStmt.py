__author__ = 'andrzejskrodzki'

from StmtBase import StmtBase
from LatteParsers.Types import *


class CondElseStmt(StmtBase):
    def __init__(self, expr, stmt1, stmt2, no_line, pos):
        super(CondElseStmt, self).__init__("condelsestmt", no_line, pos)
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def type_check(self, env):
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt1.type_check(env)
        self.stmt2.type_check(env)
        return env

    def return_check(self):
        if self.expr.value is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.value:
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()
