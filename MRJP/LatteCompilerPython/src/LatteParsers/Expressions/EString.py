__author__ = 'Andrzej Skrodzki - as292510'

from ZeroArgExpr import ZeroArgExpr
from LatteParsers.Types import *


class EString(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(EString, self).__init__(value, Type.Type("string"), no_line, pos)
        self.type = "estring"

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + self.value + " \n"
