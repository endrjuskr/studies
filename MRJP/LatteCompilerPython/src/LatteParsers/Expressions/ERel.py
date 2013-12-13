__author__ = 'Andrzej Skrodzki - as292510'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *
from LatteExceptions import *


class ERel(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(ERel, self).__init__(left, right, op, Type.Type("boolean"), None, no_line, pos)
        self.type = "erel"

    def arg_type_check(self, rtype):
        if rtype == Type.Type("boolean") and self.op != "==" and self.op != "!=":
            raise SyntaxException.SyntaxException("Boolean does not support rel operators except '==' and '!='.",
                                                  self.no_line, pos=self.pos)

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "==":
                self.value = self.left.get_value() == self.right.get_value()
            elif self.op == "!=":
                self.value = self.left.get_value() != self.right.get_value()
            elif self.op == "<=":
                self.value = self.left.get_value() <= self.right.get_value()
            elif self.op == ">=":
                self.value = self.left.get_value() >= self.right.get_value()
            elif self.op == "<":
                self.value = self.left.get_value() < self.right.get_value()
            elif self.op == ">":
                self.value = self.left.get_value() > self.right.get_value()

    def generate_body(self, env):
        s = super(ERel, self).generate_body(env)
        if self.op == "==":
            s += ""
        elif self.op == "!=":
            self.value = self.left.get_value() != self.right.get_value()
        elif self.op == "<=":
            self.value = self.left.get_value() <= self.right.get_value()
        elif self.op == ">=":
            self.value = self.left.get_value() >= self.right.get_value()
        elif self.op == "<":
            self.value = self.left.get_value() < self.right.get_value()
        elif self.op == ">":
            self.value = self.left.get_value() > self.right.get_value()

        s += "cmp" + self.line + "_" + self.pos + "_t:\n"
        s += "iconst_1 \n"
        s += "cmp" + self.line + "_" + self.pos + "_f:\n"
        s += "iconst_0 \n"
        return s