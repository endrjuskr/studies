__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.BaseNode import BaseNode

class ItemBase(BaseNode):
    def __init__(self, ident, no_line, pos, type):
        super(ItemBase, self).__init__(type, no_line, pos)
        self.ident = ident
        self.itemtype = "unknown"

    def type_check(self, env):
        pass