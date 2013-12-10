__author__ = 'andrzejskrodzki'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *
from LatteExceptions import *


class EAdd(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EAdd, self).__init__(left, right, op, None, None, no_line, pos)
        self.type = "eadd"

    def arg_type_check(self, rtype):
        if rtype == Type.Type("boolean"):
            raise SyntaxException.SyntaxException("Boolean does not support add operators.", self.no_line, pos=self.pos)
        if rtype == Type.Type("string") and self.op == "-":
            raise SyntaxException.SyntaxException("String does not support - operator.", self.no_line, pos=self.pos)

        self.etype = rtype

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "+":
                self.value = self.left.get_value() + self.right.get_value()
            elif self.op == "-":
                self.value = self.left.get_value() - self.right.get_value()
