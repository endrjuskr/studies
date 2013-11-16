__author__ = 'andrzejskrodzki'

from LatteExceptions import BaseException


class SyntaxEception(BaseException.BaseException):
    def __init__(self, inner_exception, no_line, pos=0):
        super(SyntaxEception, self).__init__(no_line, pos)
        self.inner_exception = inner_exception

    def __str__(self):
        return super(SyntaxEception, self).__str__() + "Syntax Error: " + self.inner_exception