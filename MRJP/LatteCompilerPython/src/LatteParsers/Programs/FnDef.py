__author__ = 'andrzejskrodzki'

from LatteParsers.Types.FunType import *


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