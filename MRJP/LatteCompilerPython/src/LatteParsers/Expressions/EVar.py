__author__ = 'Andrzej Skrodzki - as292510'

from ZeroArgExpr import ZeroArgExpr
from LatteExceptions import *
from LatteParsers.Types.Type import Type


class EVar(ZeroArgExpr):
    def __init__(self, ident, no_line, pos):
        super(EVar, self).__init__(ident, None, no_line, pos)
        self.type = "var"

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                raise NotDeclaredException.NotDeclaredException(self.value, False, self.no_line, self.pos)
            self.etype = env.get_variable_type(self.value)
        return self.etype

    def get_value(self):
        return None

    def generate_body(self, env):
        env.push_stack(1)
        if self.etype == Type("string"):
            return "aload " + str(env.get_variable_value(self.value)) + "\n"
        else:
            return "iload " + str(env.get_variable_value(self.value)) + "\n"