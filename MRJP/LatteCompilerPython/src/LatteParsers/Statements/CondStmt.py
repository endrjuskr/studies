__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types import *


class CondStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(CondStmt, self).__init__("condstmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt
        self.label_pattern = "cond_" + str(self.no_line) + "_" + str(self.pos)


    def type_check(self, env):
        env_prim = env.shallow_copy()
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt.type_check(env_prim)

    def return_check(self):
        if self.expr.get_value() is True:
            return self.stmt.return_check()
        else:
            return False

    def generate_body(self, env):
        env_prim = env.shallow_copy()
        s = self.expr.generate_code(env)
        s += "ifeq " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.stmt.generate_code(env_prim)
        s += self.label_pattern + ":\n"
        env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
        env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
        return s