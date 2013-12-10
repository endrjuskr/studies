__author__ = 'andrzejskrodzki'

from OneArgExpr import OneArgExpr
from LatteParsers.Types import *


class ENot(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENot, self).__init__(expr, Type.Type("boolean"), no_line, pos)
        self.type = "enot"
