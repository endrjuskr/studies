__author__ = 'andrzejskrodzki'


class NotDeclaredException(Exception):
    def __init__(self, ident, is_fun):
        self.type = "function" if is_fun else "variable"
        self.ident = ident

    def __str__(self):
        return "Not Declared Error: " + self.type + " " + self.ident + " was not declared in the scope."