__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteParsers.Types.Type import Type
from LatteExceptions import *


class AssStmt(StmtBase):
    def __init__(self, ident, expr, no_line, pos):
        super(AssStmt, self).__init__("assstmt", no_line, pos)
        self.ident = ident
        self.expr = expr
        self.idtype = None

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.idtype = env.get_variable_type(self.ident)
        self.expr.type_check(env, expected_type=self.idtype)

    def return_check(self):
        return False

    def generate_body(self, env):
        s = self.expr.generate_code(env)
        if self.idtype == Type("string"):
            s += "astore "
        else:
            s += "istore "

        s += env.get_variable_value(self.ident)
        return s