__author__ = 'andrzejskrodzki'


class BaseException(Exception):
    def __init__(self, no_line, pos):
        self.no_line = no_line
        self.pos = pos

    def __str__(self):
        return "Position - (Line:" + str(self.no_line) + ", Character:" + str(
            self.pos) + "). " if self.no_line != 0 else ""