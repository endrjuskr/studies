__author__ = 'andrzejskrodzki'


class ItemBase(object):
    def __init__(self, ident, no_line, pos, type):
        self.ident = ident
        self.itemtype = "unknown"
        self.no_line = no_line
        self.pos = pos
        self.type = type

    def type_check(self, env):
        pass