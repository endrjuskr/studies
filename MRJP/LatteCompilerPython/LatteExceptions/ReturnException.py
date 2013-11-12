__author__ = 'andrzejskrodzki'


class ReturnException(Exception):
    def __init__(self, fun_ident):
        self.fun_ident = fun_ident

    def __str__(self):
        return "Return Error: Missing return statement for function " + self.fun_ident + "."