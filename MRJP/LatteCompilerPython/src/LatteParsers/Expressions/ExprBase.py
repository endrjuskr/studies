__author__ = 'andrzejskrodzki'


class ExprBase(object):
    def __init__(self, etype, no_line, pos):
        self.no_line = no_line
        self.pos = pos
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