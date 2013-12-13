__author__ = 'Andrzej Skrodzki - as292510'

from LatteBaseException import LatteBaseException


class LexerException(LatteBaseException):
    def __init__(self, inner_exception, no_line, pos=0):
        super(LexerException, self).__init__(no_line, pos)
        self.inner_exception = inner_exception

    def __str__(self):
        return super(LexerException, self).__str__() + "Lexer Error: " + self.inner_exception