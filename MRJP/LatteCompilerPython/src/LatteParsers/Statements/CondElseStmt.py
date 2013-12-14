__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class CondElseStmt(StmtBase):
    def __init__(self, expr, stmt1, stmt2, no_line, pos):
        super(CondElseStmt, self).__init__("condelsestmt", no_line, pos)
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.label_pattern = "condelse_" + str(self.no_line) + "_" + str(self.pos)

    def type_check(self, env):
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt1.type_check(env)
        self.stmt2.type_check(env)

    def return_check(self):
        if self.expr.get_value() is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.get_value():
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()


    def generate_body(self, env):
        if self.expr.get_value() is True:
            return self.stmt1.generate_code(env)
        elif self.expr.get_value() is False:
            return self.stmt2.generate_code(env)
        else:
            s = self.expr.generate_code(env)
            s += "ifeq " + self.label_pattern + "_f\n"
            s += self.stmt1.generate_code(env)
            s += "goto " + self.label_pattern + "\n"
            s += self.label_pattern + "_f:\n"
            s += self.stmt2.generate_code(env)
            s += self.label_pattern + ":\n"
            return s