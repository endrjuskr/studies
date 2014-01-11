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
        env_prim = env.shallow_copy()
        env_prim2 = env.shallow_copy()
        self.expr.type_check(env, expected_type=Type.Type("boolean"))
        self.stmt1.type_check(env_prim)
        self.stmt2.type_check(env_prim2)

    def return_check(self):
        if self.expr.get_value() is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.get_value():
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()


    def generate_body(self, env):
        if self.expr.get_value() is True:
            env_prim = env.shallow_copy()
            s = self.stmt1.generate_code_jvm(env_prim)
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            return s
        elif self.expr.get_value() is False:
            env_prim = env.shallow_copy()
            s = self.stmt2.generate_code_jvm(env_prim)
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            return s
        else:
            env_prim = env.shallow_copy()
            env_prim2 = env.shallow_copy()
            s = self.expr.generate_code_jvm(env)
            s += "ifeq " + self.label_pattern + "_f\n"
            env.pop_stack(1)
            s += self.stmt1.generate_code_jvm(env_prim)
            s += "goto " + self.label_pattern + "\n"
            s += self.label_pattern + "_f:\n"
            s += self.stmt2.generate_code_jvm(env_prim2)
            s += self.label_pattern + ":\n"
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            env.max_variable_counter = max(env.max_variable_counter, env_prim2.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim2.max_stack_count)
            return s