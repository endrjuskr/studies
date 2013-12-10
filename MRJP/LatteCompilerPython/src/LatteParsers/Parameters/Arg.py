__author__ = 'andrzejskrodzki'


class Arg:
    def __init__(self, type, ident, no_line, pos):
        self.type = "arg"
        self.argtype = type
        self.ident = ident
        self.no_line = no_line
        self.pos = pos
