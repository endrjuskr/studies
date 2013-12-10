__author__ = 'andrzejskrodzki'

from ZeroArgExpr import ZeroArgExpr
from LatteParsers.Types import *


class EString(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(EString, self).__init__(value, Type.Type("string"), no_line, pos)
        self.type = "estring"


