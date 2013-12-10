__author__ = 'andrzejskrodzki'

from StmtBase import StmtBase


class RetStmt(StmtBase):
    def __init__(self, expr, no_line, pos):
        super(RetStmt, self).__init__("retstmt", no_line, pos)
        self.expr = expr


    def type_check(self, env):
        self.expr.type_check(env, expected_type=env.current_fun_type.returntype)
        return env

    def return_check(self):
        return True
