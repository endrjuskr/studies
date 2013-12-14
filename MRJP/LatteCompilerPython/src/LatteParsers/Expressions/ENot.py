__author__ = 'Andrzej Skrodzki - as292510'

from OneArgExpr import OneArgExpr
from LatteParsers.Types import *


class ENot(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENot, self).__init__(expr, Type.Type("boolean"), no_line, pos)
        self.type = "enot"

    def generate_body(self, env):
        s = super(ENot, self).generate_body(env)
        env.push_stack(1)
        s += "iconst_1\n"
        s += "ixor\n"
        env.pop_stack(1)
        return s