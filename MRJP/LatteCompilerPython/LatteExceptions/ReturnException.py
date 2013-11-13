__author__ = 'andrzejskrodzki'


class ReturnException(BaseException):
    def __init__(self, fun_ident, no_line):
        self.fun_ident = fun_ident
        self.no_line = no_line

    def __str__(self):
        return "Return Error: Missing return statement for function " \
               + str(self.fun_ident) + " at line - " + str(self.no_line) + "."