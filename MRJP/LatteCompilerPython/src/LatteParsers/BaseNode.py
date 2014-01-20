__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["BaseNode"]


class BaseNode(object):
    def __init__(self, type, no_line, pos):
        self.type = type
        self.no_line = no_line
        self.pos = pos
        pass

    def generate_code_jvm(self, env):
        return self.generate_header() + self.generate_body(env) + self.generate_footer()

    def generate_header(self):
        return ""

    def generate_body(self, env):
        return ""

    def generate_footer(self):
        return ""

    def generate_code_asm(self, env, get_value=True):
        return ""