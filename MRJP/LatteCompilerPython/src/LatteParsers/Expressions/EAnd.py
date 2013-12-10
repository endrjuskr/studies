__author__ = 'andrzejskrodzki'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *


class EAnd(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EAnd, self).__init__(left, right, "&&", Type.Type("boolean"), Type.Type("boolean"), no_line,
                                   pos)
        self.type = "eand"

    def calculate_value(self):
        if self.left.get_value() is False and self.left.get_value() is None:
            self.value = self.left.get_value()
        else:
            self.value = self.right.get_value()
