__author__ = 'andrzejskrodzki'

from LatteExceptions import BaseException


class ReturnException(BaseException.BaseException):
    def __init__(self, fun_ident, no_line):
        super(ReturnException, self).__init__(no_line, 0)
        self.fun_ident = fun_ident

    def __str__(self):
        return super(ReturnException, self).__str__() + "Return Error: Missing return statement for function " \
               + str(self.fun_ident) + "."