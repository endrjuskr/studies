__author__ = 'Andrzej Skrodzki - as292510'

from ZeroArgExpr import ZeroArgExpr
from LatteParsers.Types import *


class ELitBoolean(ZeroArgExpr):
    def __init__(self, lit, no_line, pos):
        super(ELitBoolean, self).__init__(True if lit == "true" else False, Type.Type("boolean"), no_line, pos)
        self.type = "elitboolean"

    def generate_body(self, env):
        return "iconst 1\n" if self.value == True else "iconst 0\n"