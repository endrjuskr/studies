__author__ = 'andrzejskrodzki'

from ZeroArgExpr import ZeroArgExpr
from LatteParsers.Types import *


class ELitInt(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(ELitInt, self).__init__(value, Type.Type("int"), no_line, pos)
        self.type = "number"
