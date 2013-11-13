__author__ = 'andrzejskrodzki'


class SyntaxEception(BaseException):
    def __init__(self, inner_exception, no_line):
        self.no_line = no_line
        self.inner_exception = inner_exception

    def __str__(self):
        return "Syntax Error: Error occured at the line " + str(self.no_line) + " - " + self.inner_exception