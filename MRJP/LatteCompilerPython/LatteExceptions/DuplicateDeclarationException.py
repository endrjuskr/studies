__author__ = 'andrzejskrodzki'


class DuplicateDeclarationException(BaseException):
    def __init__(self, ident, is_fun, no_line, pos):
        self.type = "function" if is_fun else "variable"
        self.ident = ident
        self.no_line = no_line
        self.pos = pos

    def __str__(self):
        return "Duplicate Declaration Error: " + str(self.type) + " " + str(self.ident) \
               + " was already declared in the scope at position - (L:" + str(self.no_line) \
               + ", P:" + str(self.pos) + ")."