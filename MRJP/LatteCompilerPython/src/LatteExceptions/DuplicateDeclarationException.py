__author__ = 'Andrzej Skrodzki - as292510'

from LatteBaseException import LatteBaseException


class DuplicateDeclarationException(LatteBaseException):
    def __init__(self, ident, is_fun, no_line, pos):
        super(DuplicateDeclarationException, self).__init__(no_line, pos)
        self.type = "Function" if is_fun else "Variable"
        self.ident = ident

    def __str__(self):
        return super(DuplicateDeclarationException, self).__str__() + \
               "Duplicate Declaration Error: " + str(self.type) + " " + str(self.ident) \
               + " was already declared in the scope."