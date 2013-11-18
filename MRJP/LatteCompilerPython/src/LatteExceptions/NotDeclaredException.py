__author__ = 'andrzejskrodzki'

from LatteExceptions import BaseException


class NotDeclaredException(BaseException.BaseException):
    def __init__(self, ident, is_fun, no_line, pos):
        super(NotDeclaredException, self).__init__(no_line, pos)
        self.type = "Function" if is_fun else "Variable"
        self.ident = ident

    def __str__(self):
        return super(NotDeclaredException, self).__str__() + \
               "Not Declared Error: " + str(self.type) + " " + str(self.ident) \
               + " was not declared in the scope."