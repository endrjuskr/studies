__author__ = 'Andrzej Skrodzki - as292510'

from FnDef import FnDef
from LatteParsers.Types.Type import Type
from LatteParsers.Types.FunType import FunType

class PredefinedFun(FnDef):
    def __init__(self, type, ident, arglist):
        super(PredefinedFun, self).__init__(type, ident, arglist, [], 0)

    def type_check(self, env):
        pass

    def calculate_type(self, type, arglist):
        return FunType(type, arglist)

    def generate_code(self, env):
        return ""

class ErrorFun(PredefinedFun):
    def __init__(self):
        super(ErrorFun, self).__init__(Type("void"), "error", [])

class PrintIntFun(PredefinedFun):
    def __init__(self):
        super(PrintIntFun, self).__init__(Type("void"), "printInt", [Type("int")])

class PrintStringFun(PredefinedFun):
    def __init__(self):
        super(PrintStringFun, self).__init__(Type("void"), "printString", [Type("string")])

class ReadIntFun(PredefinedFun):
    def __init__(self):
        super(ReadIntFun, self).__init__(Type("int"), "readInt", [])

class ReadStringFun(PredefinedFun):
    def __init__(self):
        super(ReadStringFun, self).__init__(Type("string"), "readString", [])

class ConcatenateStringFun(PredefinedFun):
    def __init__(self):
        super(ConcatenateStringFun, self).__init__(Type("string"), "concatenateString", [Type("string"), Type("string")])