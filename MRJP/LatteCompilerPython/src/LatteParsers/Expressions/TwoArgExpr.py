__author__ = 'andrzejskrodzki'

from ExprBase import ExprBase
from LatteExceptions import *


class TwoArgExpr(ExprBase):
    def __init__(self, left, right, op, etype, argtype, no_line, pos):
        super(TwoArgExpr, self).__init__(etype, no_line, pos)
        self.left = left
        self.right = right
        self.op = op
        self.argtype = argtype

    def type_check(self, env, expected_type=None):
        rtype = self.left.type_check(env, self.argtype)
        self.arg_type_check(rtype)
        self.right.type_check(env, rtype)

        if expected_type is not None and self.etype is not None and expected_type != self.etype:
            raise TypeException.TypeException(expected_type, self.etype, self.no_line, self.pos)
        if expected_type is not None and self.etype is None and expected_type != rtype:
            raise TypeException.TypeException(expected_type, rtype, self.no_line, self.pos)
        self.calculate_value()

        return self.etype

    def arg_type_check(self, rtype):
        pass

