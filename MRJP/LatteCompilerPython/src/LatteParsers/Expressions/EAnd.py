__author__ = 'Andrzej Skrodzki - as292510'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *


class EAnd(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EAnd, self).__init__(left, right, "&&", Type.Type("boolean"), Type.Type("boolean"), no_line,
                                   pos)
        self.type = "eand"
        self.label_pattern = "and_" + str(self.no_line) + "_" + str(self.pos)

    def calculate_value(self):
        if self.left.get_value() is False and self.left.get_value() is None:
            self.value = self.left.get_value()
        else:
            self.value = self.right.get_value()

    def generate_body(self, env):
        s = self.left.generate_code(env)
        s += "dup\n"
        s += "ifeq " + self.label_pattern + "\n"
        s += self.right.generate_code(env)
        s += "iand \n"
        s += self.label_pattern + ":\n"
        return s