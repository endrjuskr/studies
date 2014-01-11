__author__ = 'Andrzej Skrodzki - as292510'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *


class EOr(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EOr, self).__init__(left, right, "||", Type.Type("boolean"), Type.Type("boolean"), no_line,
                                  pos)
        self.type = "eor"
        self.label_pattern = "or_" + str(self.no_line) + "_" + str(self.pos)

    def calculate_value(self):
        if self.left.get_value() is True:
            self.value = True
        else:
            self.value = self.right.get_value()

    def generate_body(self, env):
        s = self.left.generate_code_jvm(env)
        s += "dup\n"
        env.push_stack(1)
        s += "ifne " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.right.generate_code_jvm(env)
        s += "ior \n"
        env.pop_stack(1)
        s += self.label_pattern + ":\n"
        return s