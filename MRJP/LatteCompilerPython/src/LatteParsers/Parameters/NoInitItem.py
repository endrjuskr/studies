__author__ = 'Andrzej Skrodzki - as292510'

from ItemBase import ItemBase
from LatteParsers.Types.Type import Type


class NoInitItem(ItemBase):
    def __init__(self, ident, no_line, pos):
        super(NoInitItem, self).__init__(ident, no_line, pos, "noinititem")

    def generate_body(self, env):
        s = ""
        env.add_variable(self.ident, self.itemtype, self.no_line, self.pos, fun_param=False)
        if self.itemtype == Type("string"):
            s += "ldc \"\" \n"
            s += "astore " + str(env.get_variable_value(self.ident)) + "\n"
        else:
            s += "iconst_0 \n"
            s += "istore " + str(env.get_variable_value(self.ident)) + "\n"

        return s