__author__ = 'andrzejskrodzki'


class Expr: pass


class EOr(Expr):
    def __init__(self, left, right):
        self.type = "eor"
        self.left = left
        self.right = right


class EAnd(Expr):
    def __init__(self, left, right):
        self.type = "eand"
        self.left = left
        self.right = right


class ERel(Expr):
    def __init__(self, left, op, right):
        self.type = "erel"
        self.left = left
        self.right = right
        self.op = op


class EAdd(Expr):
    def __init__(self, left, op, right):
        self.type = "eadd"
        self.left = left
        self.right = right
        self.op = op


class EMul(Expr):
    def __init__(self, left, op, right):
        self.type = "emul"
        self.left = left
        self.right = right
        self.op = op


class ENot(Expr):
    def __init__(self, value):
        self.type = "enot"
        self.value = value


class ENeg(Expr):
    def __init__(self, value):
        self.type = "eneg"
        self.value = value


class EString(Expr):
    def __init__(self, value):
        self.type = "estring"
        self.value = value


class EApp(Expr):
    def __init__(self, funident, exprlist):
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist


class ELitBoolean(Expr):
    def __init__(self, value):
        self.type = "elitboolean"
        self.value = value


class ELitInt(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value


class EVar(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value
