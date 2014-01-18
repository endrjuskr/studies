__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["LatteBaseException", "DuplicateDeclarationException", "LexerException", "NotDeclaredException",
           "ReturnException", "SyntaxException", "TypeException"]


class LatteBaseException(Exception):
    def __init__(self, no_line, pos):
        self.no_line = no_line
        self.pos = pos
        self.code = None
        self.column = 0

    def find_column(self):
        last_cr = self.code.rfind('\n', 0, self.pos)
        if last_cr < 0:
            last_cr = 0
        self.pos = (self.pos - last_cr) + 1

    def __str__(self):
        if self.pos != 0:
            self.find_column()
        return "(Line:" + str(self.no_line) + ", Character:" + str(self.pos) + ") " if self.no_line != -1 else ""


class DuplicateDeclarationException(LatteBaseException):
    def __init__(self, ident, is_fun, no_line, pos):
        super(DuplicateDeclarationException, self).__init__(no_line, pos)
        self.type = "Function" if is_fun else "Variable"
        self.ident = ident

    def __str__(self):
        return super(DuplicateDeclarationException, self).__str__() + \
            "Duplicate Declaration Error: " + str(self.type) + " " + str(self.ident) \
            + " was already declared in the scope."


class LexerException(LatteBaseException):
    def __init__(self, inner_exception, no_line, pos=0):
        super(LexerException, self).__init__(no_line, pos)
        self.inner_exception = inner_exception

    def __str__(self):
        return super(LexerException, self).__str__() + "Lexer Error: " + self.inner_exception


class NotDeclaredException(LatteBaseException):
    def __init__(self, ident, is_fun, no_line, pos):
        super(NotDeclaredException, self).__init__(no_line, pos)
        self.type = "Function" if is_fun else "Variable"
        self.ident = ident

    def __str__(self):
        return super(NotDeclaredException, self).__str__() + \
            "Not Declared Error: " + str(self.type) + " " + str(self.ident) \
            + " was not declared in the scope."


class ReturnException(LatteBaseException):
    def __init__(self, fun_ident, no_line):
        super(ReturnException, self).__init__(no_line, 0)
        self.fun_ident = fun_ident

    def __str__(self):
        return super(ReturnException, self).__str__() + "Return Error: Missing return statement for function " \
            + str(self.fun_ident) + "."


class SyntaxException(LatteBaseException):
    def __init__(self, inner_exception, no_line, pos=0):
        super(SyntaxException, self).__init__(no_line, pos)
        self.inner_exception = inner_exception

    def __str__(self):
        return super(SyntaxException, self).__str__() + "Syntax Error: " + self.inner_exception


class TypeException(LatteBaseException):
    def __init__(self, expected_type, received_type, no_line, pos):
        super(TypeException, self).__init__(no_line, pos)
        self.expected_type = expected_type
        self.received_type = received_type

    def __str__(self):
        return super(TypeException, self).__str__() \
               + "Type Error: Expected type is " + str(self.expected_type) + ", but " \
               + str(self.received_type) + " was received."