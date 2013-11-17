__author__ = 'andrzejskrodzki'

from LatteExceptions import BaseException


class SyntaxException(BaseException.BaseException):
    def __init__(self, inner_exception, no_line, pos=0):
        super(SyntaxException, self).__init__(no_line, pos)
        self.inner_exception = inner_exception

    def __str__(self):
        return super(SyntaxException, self).__str__() + "Syntax Error: " + self.inner_exception