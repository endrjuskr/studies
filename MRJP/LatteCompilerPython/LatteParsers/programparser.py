__author__ = 'andrzejskrodzki'

from LatteParsers.typeparser import FunType


class Program:
    def __init__(self, topdeflist):
        self.type = "program"
        self.topdeflist = topdeflist


class FnDef:
    def __init__(self, type, ident, arglist, block):
        self.type = "fndef"
        self.funtype = self.calculate_type(type, arglist)
        self.ident = ident
        self.arglist = arglist
        self.block = block

    def get_type(self, arg):
        return arg.argtype

    def calculate_type(self, type, arglist):
        return FunType(type, map(self.get_type, arglist))


class Arg:
    def __init__(self, type, ident):
        self.type = "arg"
        self.argtype = type
        self.ident = ident
