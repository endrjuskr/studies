__author__ = 'andrzejskrodzki'


class SyntaxEception(Exception):
    def __init__(self, no_line, inner_exception):
        self.no_line = no_line
        self.inner_exception = inner_exception

    def __str__(self):
        return "Syntax Error: Error occured at the line " + self.no_line + " - " + self.inner_exception