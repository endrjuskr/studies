__author__ = 'andrzejskrodzki'


class Type():
    def __init__(self, value):
        self.type = value
        self.value = value


class FunType(Type):
    def __init__(self, returntype, paramstypes):
        self.type = "funtype"
        self.returntype = returntype
        self.paramstypes = paramstypes