__author__ = 'Andrzej Skrodzki - as292510'

from ItemBase import ItemBase
from LatteParsers.Types.Type import Type


class InitItem(ItemBase):
    def __init__(self, ident, expr, no_line, pos):
        super(InitItem, self).__init__(ident, no_line, pos, "inititem")
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env, expected_type=self.itemtype)

    def generate_body(self, env):
        s = self.expr.generate_body(env)
        if self.itemtype == Type("string"):
            s += "astore " + str(env.get_variable_value(self.ident)) + "\n"
        else:
            s += "istore " + str(env.get_variable_value(self.ident)) + "\n"
        return s