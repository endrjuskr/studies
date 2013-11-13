__author__ = 'andrzejskrodzki'

import typeparser
from LatteExceptions import TypeException, SyntaxException, NotDeclaredException

class Expr:
    pass


class EOr(Expr):
    def __init__(self, left, right, no_line):
        self.type = "eor"
        self.left = left
        self.right = right
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, typeparser.Type("boolean"), self.no_line)
        self.left.type_check(env, expected_type)
        self.right.type_check(env, expected_type)

        if self.left.value is True:
            self.value = True
        else:
            self.value = self.right.value


class EAnd(Expr):
    def __init__(self, left, right, no_line):
        self.type = "eand"
        self.left = left
        self.right = right
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, typeparser.Type("boolean"), self.no_line)
        self.left.type_check(env, typeparser.Type("boolean"))
        self.right.type_check(env, typeparser.Type("boolean"))

        if self.left.value is False and self.left.value is None:
            self.value = self.left.value
        else:
            self.value = self.right.value

        return typeparser.Type("boolean")



class ERel(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "erel"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        return_type = self.left.type_check(env, None)

        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, typeparser.Type("boolean"), self.no_line)

        self.right.type_check(env, return_type)

        if self.left.value is not None and self.right.value is not None:
            if self.op == "==":
                self.value = self.left.value == self.right.value
            elif self.op == "<=":
                self.value = self.left.value <= self.right.value
            elif self.op == ">=":
                self.value = self.left.value <= self.right.value
            elif self.op == "<":
                self.value = self.left.value < self.right.value
            elif self.op == ">":
                self.value = self.left.value > self.right.value

        return typeparser.Type("boolean")

    def return_check(self):
        return False


class EAdd(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "eadd"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        returned_type = self.left.type_check(env, expected_type)
        if expected_type is not None and expected_type == typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, returned_type, self.no_line)
        if expected_type is not None and expected_type == typeparser.Type("string") and self.op == "-":
            raise SyntaxException.SyntaxEception("String does not support - operator.", self.no_line)
        self.right.type_check(env, returned_type)

        if self.left.value is not None and self.right.value is not None:
            if self.op == "+":
                self.value = self.left.value + self.right.value
            elif self.op == "-":
                self.value = self.left.value - self.right.value
        return returned_type


class EMul(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "emul"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("int"):
            raise TypeException.TypeException(expected_type, typeparser.Type("int"), self.no_line)
        self.left.type_check(env, typeparser.Type("int"))
        self.right.type_check(env, typeparser.Type("int"))
        if self.left.value is not None and self.right.value is not None:
            if self.op == "/":
                if self.right.value == 0:
                    raise SyntaxException.SyntaxEception("Division by 0", self.no_line)
                self.value = self.left.value / self.right.value
            elif self.op == "*":
                self.value = self.left.value * self.right.value
            elif self.op == "%":
                if self.right.value == 0:
                    raise SyntaxException.SyntaxEception("Modulo by 0", self.no_line)
                self.value = self.left.value % self.right.value

        return typeparser.Type("int")


class ENot(Expr):
    def __init__(self, expr, no_line):
        self.type = "enot"
        self.expr = expr
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, typeparser.Type("boolean"), self.no_line)
        self.expr.type_check(env, typeparser.Type("boolean"))

        if self.expr.value is not None:
            self.value = not self.expr.value

        return typeparser.Type("boolean")


class ENeg(Expr):
    def __init__(self, expr, no_line):
        self.type = "eneg"
        self.expr = expr
        self.no_line = no_line
        self.value = None

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("int"):
            raise TypeException.TypeException(expected_type, typeparser.Type("int"), self.no_line)
        self.expr.type_check(env, typeparser.Type("int"))
        if self.expr.value is not None:
            self.value = - self.expr.value
        return typeparser.Type("int")


class EString(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "estring"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("string"):
            raise TypeException.TypeException(expected_type, typeparser.Type("string"), self.no_line)

        return typeparser.Type("string")


class EApp(Expr):
    def __init__(self, funident, exprlist, no_line, pos):
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist
        self.no_line = no_line
        self.pos = pos
        self.value = None

    def type_check(self, env, expected_type=None):
        if not env.contain_funtion(self.funident):
            raise NotDeclaredException.NotDeclaredException(self.funident, True, self.no_line, self.pos)

        fun_type = env.get_fun_type(self.funident)
        if expected_type is not None and expected_type != fun_type.returntype:
            raise TypeException.TypeException(expected_type, fun_type.returntype, self.no_line)

        if len(self.exprlist) != len(fun_type.paramstypes):
            raise SyntaxException.SyntaxEception("Wrong number of parameters for function "
                                                 + self.funident + " - expected:"
                                                 + str(len(fun_type.paramstypes)) + " actual: "
                                                 + str(len(self.exprlist)) + ".", self.no_line)

        for i in range(len(self.exprlist)):
            self.exprlist[i].type_check(env, fun_type.paramstypes[i])
        return fun_type.returntype


class ELitBoolean(Expr):
    def __init__(self, lit, no_line, pos):
        self.type = "elitboolean"
        self.value = True if lit == "true" else False
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            raise TypeException.TypeException(expected_type, typeparser.Type("boolean"), self.no_line)
        return typeparser.Type("boolean")


class ELitInt(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "number"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("int"):
            raise TypeException.TypeException(expected_type, typeparser.Type("int"), self.no_line)
        return typeparser.Type("int")


class EVar(Expr):
    def __init__(self, ident, no_line, pos):
        self.type = "number"
        self.ident = ident
        self.no_line = no_line
        self.pos = pos
        self.value = None

    def type_check(self, env, expected_type=None):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)

        var_type = env.get_variable_type(self.ident)
        if expected_type is not None and expected_type != var_type:
            raise TypeException.TypeException(expected_type, var_type, self.no_line)

        return var_type