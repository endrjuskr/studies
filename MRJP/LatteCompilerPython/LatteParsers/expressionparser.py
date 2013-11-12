__author__ = 'andrzejskrodzki'

import typeparser


class Expr: pass


class EOr(Expr):
    def __init__(self, left, right, no_line):
        self.type = "eor"
        self.left = left
        self.right = right
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            print "Expected " + expected_type + ", but got boolean. At line: " + str(self.no_line)
            exit(-1)
        self.left.type_check(env, expected_type)
        self.right.type_check(env, expected_type)


class EAnd(Expr):
    def __init__(self, left, right, no_line):
        self.type = "eand"
        self.left = left
        self.right = right
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            print "Expected " + expected_type + ", but got boolean. At line: " + str(self.no_line)
            exit(-1)
        self.left.type_check(env, typeparser.Type("boolean"))
        self.right.type_check(env, typeparser.Type("boolean"))
        return typeparser.Type("boolean")


class ERel(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "erel"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        print expected_type, self.no_line
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            print "Expected " + str(expected_type) + ", but got boolean. At line: " + str(self.no_line)
            exit(-1)

        returntype = self.left.type_check(env, None)
        self.right.type_check(env, returntype)
        return typeparser.Type("boolean")


class EAdd(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "eadd"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type == typeparser.Type("boolean"):
            print "Expected " + expected_type + ", but got not boolean. At line: " + str(self.no_line)
            exit(-1)
        if expected_type is not None and expected_type == typeparser.Type("string") and self.op == "-":
            print "String does not support - operator."
            exit(-1)
        returned_type = self.left.type_check(env, expected_type)
        self.right.type_check(env, returned_type)
        return returned_type


class EMul(Expr):
    def __init__(self, left, op, right, no_line):
        self.type = "emul"
        self.left = left
        self.right = right
        self.op = op
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        print expected_type
        if expected_type is not None and expected_type != typeparser.Type("int"):
            print "Expected " + expected_type + ", but got integer. At line: " + str(self.no_line)
            exit(-1)
        self.left.type_check(env, typeparser.Type("int"))
        self.right.type_check(env, typeparser.Type("int"))
        return typeparser.Type("int")


class ENot(Expr):
    def __init__(self, value, no_line):
        self.type = "enot"
        self.value = value
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            print "Expected " + expected_type + ", but got boolean. At line: " + str(self.no_line)
            exit(-1)
        self.value.type_check(env, typeparser.Type("boolean"))
        return typeparser.Type("boolean")


class ENeg(Expr):
    def __init__(self, value, no_line):
        self.type = "eneg"
        self.value = value
        self.no_line = no_line

    def type_check(self, env, expected_type=None):
        print expected_type
        if expected_type is not None and expected_type != typeparser.Type("int"):
            print "Expected " + expected_type + ", but got integer. At line: " + str(self.no_line)
            exit(-1)
        self.value.type_check(env, typeparser.Type("int"))
        return typeparser.Type("int")


class EString(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "estring"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("string"):
            print "Expected " + expected_type + ", but got string. At line: " + str(self.no_line)
            exit(-1)
        return typeparser.Type("string")


class EApp(Expr):
    def __init__(self, funident, exprlist, no_line, pos):
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if not env.contain_ident(self.funident):
            print "Funtion " + self.funident + " is not declared."
            exit(-1)

        fun_type = env.get_fun_type(self.funident)
        if expected_type is not None and expected_type != fun_type.returntype:
            print "Expected " + str(expected_type) + ", but got " + str(fun_type.returntype) + ". At line: " + str(
                self.no_line)
            exit(-1)

        if len(self.exprlist) != len(fun_type.paramstypes):
            print "Wrong number of parameters. At line: " + str(
                self.no_line), self.funident, len(self.exprlist), len(fun_type.paramstypes)
            exit(-1)

        for i in range(len(self.exprlist)):
            self.exprlist[i].type_check(env, fun_type.paramstypes[i])
        return fun_type.returntype


class ELitBoolean(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "elitboolean"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("boolean"):
            print "Expected " + str(expected_type) + ", but got boolean. At line: " + str(self.no_line)
            exit(-1)
        return typeparser.Type("boolean")


class ELitInt(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "number"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != typeparser.Type("int"):
            print "Expected " + str(expected_type) + ", but got int. At line: " + str(self.no_line)
            exit(-1)
        return typeparser.Type("int")


class EVar(Expr):
    def __init__(self, value, no_line, pos):
        self.type = "number"
        self.value = value
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env, expected_type=None):
        if not env.contain_ident(self.value):
            print "Variable " + self.value + " is not declared."
            exit(-1)

        var_type = env.get_variable_type(self.value)
        print self.no_line, var_type
        if expected_type is not None and expected_type != var_type:
            print "Expected " + str(expected_type) + ", but got " + str(var_type) + ". At line: " + str(self.no_line)
            exit(-1)

        return var_type