__author__ = 'andrzejskrodzki'


class BaseException(Exception):
    def __init__(self, no_line, pos):
        self.no_line = no_line
        self.pos = pos

    def __str__(self):
        return "(Line:" + str(self.no_line) + ") " if self.no_line != -1 else ""