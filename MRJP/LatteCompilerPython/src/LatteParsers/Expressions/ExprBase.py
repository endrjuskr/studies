__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.BaseNode import BaseNode

class ExprBase(BaseNode):
    def __init__(self, etype, no_line, pos):
        super(ExprBase, self).__init__("expr", no_line, pos)
        self.value = None
        self.etype = etype

    def type_check(self, env, expected_type=None):
        return None

    def calculate_value(self):
        pass

    def return_check(self):
        return False

    def get_value(self):
        return self.value