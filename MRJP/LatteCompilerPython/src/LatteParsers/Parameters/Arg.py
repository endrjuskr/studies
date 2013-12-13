__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.BaseNode import BaseNode

class Arg(BaseNode):
    def __init__(self, type, ident, no_line, pos):
        super(Arg, self).__init__("arg", no_line, pos)
        self.argtype = type
        self.ident = ident
