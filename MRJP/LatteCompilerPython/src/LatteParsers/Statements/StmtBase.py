__author__ = 'andrzejskrodzki'


class StmtBase(object):
    def __init__(self, type, no_line, pos):
        self.type = type
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        return env

    def return_check(self):
        return False
