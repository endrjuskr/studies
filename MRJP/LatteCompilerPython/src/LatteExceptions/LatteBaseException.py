__author__ = 'Andrzej Skrodzki - as292510'


class LatteBaseException(Exception):
    def __init__(self, no_line, pos):
        self.no_line = no_line
        self.pos = pos
        self.column = None

    def find_column(self, input):
        if self.pos == 0:
            return
        last_cr = input.rfind('\n', 0, self.pos)
        if last_cr < 0:
            last_cr = 0
        self.column = (self.pos - last_cr) + 1

    def __str__(self):
        if self.column is None:
            self.column = 0
        return "(Line:" + str(self.no_line) + ", Character:" + str(self.column) + ") " if self.no_line != -1 else ""