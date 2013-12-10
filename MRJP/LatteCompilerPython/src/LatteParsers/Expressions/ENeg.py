__author__ = 'andrzejskrodzki'

from OneArgExpr import OneArgExpr
from LatteParsers.Types import *


class ENeg(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENeg, self).__init__(expr, Type.Type("int"), no_line, pos)
        self.type = "eneg"
