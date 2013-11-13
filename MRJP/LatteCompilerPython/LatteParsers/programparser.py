__author__ = 'andrzejskrodzki'

from LatteParsers.typeparser import FunType


class Program:
    def __init__(self, topdeflist):
        self.type = "program"
        self.topdeflist = topdeflist


class FnDef:
    def __init__(self, type, ident, arglist, block, no_line):
        self.type = "fndef"
        self.funtype = self.calculate_type(type, arglist)
        self.ident = ident
        self.arglist = arglist
        self.block = block
        self.no_line = no_line

    def get_type(self, arg):
        return arg.argtype

    def calculate_type(self, type, arglist):
        return FunType(type, map(self.get_type, arglist))


class Arg:
    def __init__(self, type, ident, no_line, pos):
        self.type = "arg"
        self.argtype = type
        self.ident = ident
        self.no_line = no_line
        self.pos = pos
