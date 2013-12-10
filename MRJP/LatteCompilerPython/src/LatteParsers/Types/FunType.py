__author__ = 'andrzejskrodzki'

from Type import Type
from operator import eq


class FunType(Type):
    def __init__(self, returntype, paramstypes):
        super(FunType, self).__init__("funtype")
        self.returntype = returntype
        self.paramstypes = paramstypes

    def __eq__(self, other):
        return self.returntype == other.returntype and len(self.paramstypes) == len(other.paramstypes) and all(
            map(eq, self.paramstypes, other.paramstypes))

    def __str__(self):
        return "(" + str(self.returntype) + ", " + str(self.paramstypes) + ")"

    def isFunction(self):
        return True