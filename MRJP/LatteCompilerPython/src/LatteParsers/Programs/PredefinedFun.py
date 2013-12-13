__author__ = 'Andrzej Skrodzki - as292510'

from FnDef import FnDef

class PredefinedFun(FnDef):
    def __init__(self, type, ident, arglist):
        super(PredefinedFun, self).__init__(type, ident, arglist, [], 0)

    def type_check(self):
        pass