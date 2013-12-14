__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class WhileStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(WhileStmt, self).__init__("whilestmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt
        self.label_pattern = "while_" + str(self.no_line) + "_" + str(self.pos)

    def type_check(self, env):
        env_prim = env.shallow_copy()
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt.type_check(env_prim)

    def return_check(self):
        return self.stmt.return_check()

    def generate_body(self, env):
        env_prim = env.shallow_copy()
        s = self.label_pattern + "_w:\n"
        s += self.expr.generate_code(env)
        s += "ifeq " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.stmt.generate_code(env_prim)
        s += "goto " + self.label_pattern + "_w\n"
        s += self.label_pattern + ":\n"
        env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
        env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
        return s
