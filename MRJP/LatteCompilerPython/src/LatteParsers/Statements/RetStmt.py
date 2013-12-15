__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types.Type import Type


class RetStmt(StmtBase):
    def __init__(self, expr, no_line, pos):
        super(RetStmt, self).__init__("retstmt", no_line, pos)
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env, expected_type=env.current_fun_type.returntype)

    def return_check(self):
        return True

    def generate_body(self, env):
        s = self.expr.generate_code(env)
        if env.in_main:
            s += "invokestatic java/lang/System/exit(I)V\n"
            s += "return\n"
        elif env.current_fun_type.returntype == Type("string"):
            s += "areturn \n"
        else:
            s += "ireturn \n"
        env.pop_stack(1)
        return s