__author__ = 'andrzejskrodzki'

from ZeroArgExpr import ZeroArgExpr
from LatteParsers.Types import *


class ELitBoolean(ZeroArgExpr):
    def __init__(self, lit, no_line, pos):
        super(ELitBoolean, self).__init__(True if lit == "true" else False, Type.Type("boolean"), no_line, pos)
        self.type = "elitboolean"
