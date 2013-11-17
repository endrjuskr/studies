__author__ = 'andrzejskrodzki'
from operator import eq


class Type():
    def __init__(self, value):
        self.type = value
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __str__(self):
        return self.value

    def isFunction(self):
        return False


class FunType(Type):
    def __init__(self, returntype, paramstypes):
        self.type = "funtype"
        self.returntype = returntype
        self.paramstypes = paramstypes

    def __eq__(self, other):
        return self.returntype == other.returntype and len(self.paramstypes) == len(other.paramstypes) and all(
            map(eq, self.paramstypes, other.paramstypes))

    def __str__(self):
        return "(" + str(self.returntype) + ", " + str(self.paramstypes) + ")"

    def isFunction(self):
        return True