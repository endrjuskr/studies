__author__ = 'andrzejskrodzki'

import typeparser
from LatteExceptions import TypeException, SyntaxException, NotDeclaredException


class Expr(object):
    def __init__(self, etype, no_line, pos):
        self.no_line = no_line
        self.pos = pos
        self.value = None
        self.etype = etype

    def type_check(self, env, expected_type=None):
        return None

    def calculate_value(self):
        pass

    def return_check(self):
        return False

    def get_value(self):
        return self.value


class TwoArgExpr(Expr):
    def __init__(self, left, right, op, etype, argtype, no_line, pos):
        super(TwoArgExpr, self).__init__(etype, no_line, pos)
        self.left = left
        self.right = right
        self.op = op
        self.argtype = argtype

    def type_check(self, env, expected_type=None):
        # print self.left, self.right, self.op, self.no_line
        # print "left"
        rtype = self.left.type_check(env, self.argtype)
        self.arg_type_check(rtype)
        # print "right", self.right
        self.right.type_check(env, rtype)

        if expected_type is not None and self.etype is not None and expected_type != self.etype:
            raise TypeException.TypeException(expected_type, self.etype, self.no_line, self.pos)
        if expected_type is not None and self.etype is None and expected_type != rtype:
            raise TypeException.TypeException(expected_type, rtype, self.no_line, self.pos)
        self.calculate_value()

        return self.etype

    def arg_type_check(self, rtype):
        pass


class OneArgExpr(Expr):
    def __init__(self, expr, etype, no_line, pos):
        super(OneArgExpr, self).__init__(etype, no_line, pos)
        self.expr = expr

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.etype:
            raise TypeException.TypeException(expected_type, self.etype, self.no_line, self.pos)
            # print "oneorg"
        self.expr.type_check(env, self.etype)
        return self.etype

    def calculate_value(self):
        if self.expr.value is not None:
            self.value = - self.expr.value


class ZeroArgExpr(Expr):
    def __init__(self, value, etype, no_line, pos):
        super(ZeroArgExpr, self).__init__(etype, no_line, pos)
        self.value = value

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.get_type(env):
            raise TypeException.TypeException(expected_type, self.get_type(env), self.no_line, self.pos)

        return self.get_type(env)

    def get_type(self, env):
        return self.etype


class EOr(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EOr, self).__init__(left, right, "||", typeparser.Type("boolean"), typeparser.Type("boolean"), no_line,
                                  pos)
        self.type = "eor"

    def calculate_value(self):
        if self.left.get_value() is True:
            self.value = True
        else:
            self.value = self.right.get_value()


class EAnd(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EAnd, self).__init__(left, right, "&&", typeparser.Type("boolean"), typeparser.Type("boolean"), no_line,
                                   pos)
        self.type = "eand"

    def calculate_value(self):
        if self.left.get_value() is False and self.left.get_value() is None:
            self.value = self.left.get_value()
        else:
            self.value = self.right.get_value()


class ERel(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(ERel, self).__init__(left, right, op, typeparser.Type("boolean"), None, no_line, pos)
        self.type = "erel"

    def arg_type_check(self, rtype):
        if rtype == typeparser.Type("boolean") and self.op != "==" and self.op != "!=":
            raise SyntaxException.SyntaxException("Boolean does not support rel operators except '==' and '!='.",
                                                  self.no_line, pos=self.pos)

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "==":
                self.value = self.left.get_value() == self.right.get_value()
            elif self.op == "!=":
                self.value = self.left.get_value() != self.right.get_value()
            elif self.op == "<=":
                self.value = self.left.get_value() <= self.right.get_value()
            elif self.op == ">=":
                self.value = self.left.get_value() >= self.right.get_value()
            elif self.op == "<":
                self.value = self.left.get_value() < self.right.get_value()
            elif self.op == ">":
                self.value = self.left.get_value() > self.right.get_value()


class EAdd(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EAdd, self).__init__(left, right, op, None, None, no_line, pos)
        self.type = "eadd"

    def arg_type_check(self, rtype):
        if rtype == typeparser.Type("boolean"):
            raise SyntaxException.SyntaxException("Boolean does not support add operators.", self.no_line, pos=self.pos)
        if rtype == typeparser.Type("string") and self.op == "-":
            raise SyntaxException.SyntaxException("String does not support - operator.", self.no_line, pos=self.pos)

        self.etype = rtype

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "+":
                self.value = self.left.get_value() + self.right.get_value()
            elif self.op == "-":
                self.value = self.left.get_value() - self.right.get_value()


class EMul(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EMul, self).__init__(left, right, op, typeparser.Type("int"), typeparser.Type("int"), no_line, pos)
        self.type = "emul"


    def calculate_value(self):
        #print self.op, self.right, self.left, self.no_line
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "/":
                if self.right.get_value() == 0:
                    raise SyntaxException.SyntaxException("Division by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() / self.right.get_value()
            elif self.op == "*":
                self.value = self.left.get_value() * self.right.get_value()
            elif self.op == "%":
                if self.right.get_value() == 0:
                    raise SyntaxException.SyntaxException("Modulo by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() % self.right.get_value()


class ENot(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENot, self).__init__(expr, typeparser.Type("boolean"), no_line, pos)
        self.type = "enot"


class ENeg(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENeg, self).__init__(expr, typeparser.Type("int"), no_line, pos)
        self.type = "eneg"


class EString(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(EString, self).__init__(value, typeparser.Type("string"), no_line, pos)
        self.type = "estring"


class EApp(ZeroArgExpr):
    def __init__(self, funident, exprlist, no_line, pos):
        super(EApp, self).__init__(None, None, no_line, pos)
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_funtion(self.funident):
                raise NotDeclaredException.NotDeclaredException(self.funident, True, self.no_line, self.pos)
            self.etype = env.get_fun_type(self.funident)
            self.check_arg_list(env)

        return self.etype.returntype

    def check_arg_list(self, env):
        if len(self.exprlist) != len(self.etype.paramstypes):
            raise SyntaxException.SyntaxException("Wrong number of parameters for function "
                                                 + self.funident + " - expected:"
                                                 + str(len(self.etype.paramstypes)) + " actual: "
                                                 + str(len(self.exprlist)) + ".", self.no_line, pos=self.pos)

        for i in range(len(self.exprlist)):
            #print "arg"
            self.exprlist[i].type_check(env, self.etype.paramstypes[i])


class ELitBoolean(ZeroArgExpr):
    def __init__(self, lit, no_line, pos):
        super(ELitBoolean, self).__init__(True if lit == "true" else False, typeparser.Type("boolean"), no_line, pos)
        self.type = "elitboolean"


class ELitInt(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(ELitInt, self).__init__(value, typeparser.Type("int"), no_line, pos)
        self.type = "number"


class EVar(ZeroArgExpr):
    def __init__(self, ident, no_line, pos):
        super(EVar, self).__init__(ident, None, no_line, pos)
        self.type = "var"

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                raise NotDeclaredException.NotDeclaredException(self.value, False, self.no_line, self.pos)
            self.etype = env.get_variable_type(self.value)
        return self.etype

    def get_value(self):
        return None