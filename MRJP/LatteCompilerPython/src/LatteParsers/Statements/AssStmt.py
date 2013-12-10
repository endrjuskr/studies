__author__ = 'andrzejskrodzki'

from StmtBase import StmtBase
from LatteExceptions import *


class AssStmt(StmtBase):
    def __init__(self, ident, expr, no_line, pos):
        super(AssStmt, self).__init__("assstmt", no_line, pos)
        self.ident = ident
        self.expr = expr

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.expr.type_check(env, expected_type=env.get_variable_type(self.ident))
        return env

    def return_check(self):
        return False