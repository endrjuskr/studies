__author__ = 'Andrzej Skrodzki - as292510'

from ExprBase import ExprBase
from LatteExceptions import *


class OneArgExpr(ExprBase):
    def __init__(self, expr, etype, no_line, pos):
        super(OneArgExpr, self).__init__(etype, no_line, pos)
        self.expr = expr

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.etype:
            raise TypeException.TypeException(expected_type, self.etype, self.no_line, self.pos)
        self.expr.type_check(env, self.etype)
        return self.etype

    def calculate_value(self):
        if self.expr.value is not None:
            self.value = - self.expr.value

    def generate_body(self, env):
        s = self.expr.generate_code_jvm(env)
        return s