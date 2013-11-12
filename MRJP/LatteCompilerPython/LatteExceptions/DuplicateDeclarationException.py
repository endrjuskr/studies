__author__ = 'andrzejskrodzki'


class DuplicateDeclarationException(Exception):
    def __init__(self, ident, is_fun):
        self.type = "function" if is_fun else "variable"
        self.ident = ident

    def __str__(self):
        return "Duplicate Declaration Error: " + self.type + " " + self.ident + " was already declared in the scope."