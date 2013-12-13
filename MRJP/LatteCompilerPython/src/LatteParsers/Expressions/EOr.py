__author__ = 'Andrzej Skrodzki - as292510'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *


class EOr(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EOr, self).__init__(left, right, "||", Type.Type("boolean"), Type.Type("boolean"), no_line,
                                  pos)
        self.type = "eor"

    def calculate_value(self):
        if self.left.get_value() is True:
            self.value = True
        else:
            self.value = self.right.get_value()

    def generate_body(self, env):
        s = super(EOr, self).generate_body(env)
        s += "ior \n"
        return s