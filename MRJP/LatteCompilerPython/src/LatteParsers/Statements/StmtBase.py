__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.BaseNode import BaseNode

class StmtBase(BaseNode):
    def __init__(self, type, no_line, pos):
        super(StmtBase, self).__init__(type, no_line, pos)


    def type_check(self, env):
        pass

    def return_check(self):
        return False
