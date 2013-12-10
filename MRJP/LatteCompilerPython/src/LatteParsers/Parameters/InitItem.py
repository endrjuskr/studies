__author__ = 'andrzejskrodzki'

from ItemBase import ItemBase


class InitItem(ItemBase):
    def __init__(self, ident, expr, no_line, pos):
        super(InitItem, self).__init__(ident, no_line, pos, "inititem")
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env, expected_type=self.itemtype)