__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class WhileStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(WhileStmt, self).__init__("whilestmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt
        self.label_pattern = "while_" + self.no_line + "_" + self.pos

    def type_check(self, env):
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt.type_check(env)

    def return_check(self):
        return self.stmt.return_check()

    def generate_body(self, env):
        s = self.label_pattern + "_w:\n"
        s += self.expr.generate_code(env)
        s += "ifeq " + self.label_pattern + "\n"
        s += self.stmt.generate_code(env)
        s += "goto " + self.label_pattern + "_w\n"
        s += self.label_pattern + ":\n"
        return s
