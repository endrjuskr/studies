__author__ = 'Andrzej Skrodzki - as292510'

from OneArgExpr import OneArgExpr
from LatteParsers.Types import *


class ENot(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENot, self).__init__(expr, Type.Type("boolean"), no_line, pos)
        self.type = "enot"

    def generate_body(self, env):
        s = super(ENot, self).generate_body(env)
        s += "dup \n"
        s += "ixor \n"
        return s