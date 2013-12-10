__author__ = 'andrzejskrodzki'

from ExprBase import ExprBase
from LatteExceptions import *


class ZeroArgExpr(ExprBase):
    def __init__(self, value, etype, no_line, pos):
        super(ZeroArgExpr, self).__init__(etype, no_line, pos)
        self.value = value

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.get_type(env):
            raise TypeException.TypeException(expected_type, self.get_type(env), self.no_line, self.pos)

        return self.get_type(env)

    def get_type(self, env):
        return self.etype