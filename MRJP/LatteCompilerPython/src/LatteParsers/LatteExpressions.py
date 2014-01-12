__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["EAdd", "EAnd", "EApp", "ELitBoolean", "ELitInt", "EMul", "ENeg", "ENot", "EOr", "ERel", "EString", "EVar",
           "ExprBase", "OneArgExpr", "TwoArgExpr", "ZeroArgExpr", "EArrayInit", "EArrayApp", "EObjectInit",
           "ELitNull", "EObjectField", "EObjectApp"]

from .BaseNode import *
from ..LatteExceptions import *
from .LatteTypes import *


class ExprBase(BaseNode):
    def __init__(self, etype, no_line, pos):
        super(ExprBase, self).__init__("expr", no_line, pos)
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


class OneArgExpr(ExprBase):
    def __init__(self, expr, etype, no_line, pos):
        super(OneArgExpr, self).__init__(etype, no_line, pos)
        self.expr = expr

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.etype:
            raise TypeException(expected_type, self.etype, self.no_line, self.pos)
        self.expr.type_check(env, self.etype)
        return self.etype

    def calculate_value(self):
        if self.expr.value is not None:
            self.value = - self.expr.value

    def generate_body(self, env):
        s = self.expr.generate_code_jvm(env)
        return s

    def generate_code_asm(self, env):
        return self.expr.generate_code_asm(env)


class TwoArgExpr(ExprBase):
    def __init__(self, left, right, op, etype, argtype, no_line, pos):
        super(TwoArgExpr, self).__init__(etype, no_line, pos)
        self.left = left
        self.right = right
        self.op = op
        self.argtype = argtype

    def type_check(self, env, expected_type=None):
        rtype = self.left.type_check(env, self.argtype)
        self.arg_type_check(rtype)
        self.right.type_check(env, rtype)

        if expected_type is not None and self.etype is not None and expected_type != self.etype:
            raise TypeException(expected_type, self.etype, self.no_line, self.pos)
        if expected_type is not None and self.etype is None and expected_type != rtype:
            raise TypeException(expected_type, rtype, self.no_line, self.pos)
        self.calculate_value()

        return self.etype

    def arg_type_check(self, rtype):
        pass

    def generate_body(self, env):
        s = self.left.generate_code_jvm(env)
        s += self.right.generate_code_jvm(env)
        return s

    def generate_code_asm(self, env):
        s = self.left.generate_code_asm(env)
        reg = env.get_free_registry()
        s += "mov " + reg + ", rax"
        s += self.left.generate_code_asm(env)



class ZeroArgExpr(ExprBase):
    def __init__(self, value, etype, no_line, pos):
        super(ZeroArgExpr, self).__init__(etype, no_line, pos)
        self.value = value

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.get_type(env):
            raise TypeException(expected_type, self.get_type(env), self.no_line, self.pos)

        return self.get_type(env)

    def get_type(self, env):
        return self.etype


class EAdd(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EAdd, self).__init__(left, right, op, None, None, no_line, pos)
        self.type = "eadd"

    def arg_type_check(self, rtype):
        if rtype == Type("boolean"):
            raise SyntaxException("Boolean does not support add operators.", self.no_line, pos=self.pos)
        if rtype == Type("string") and self.op == "-":
            raise SyntaxException("String does not support - operator.", self.no_line, pos=self.pos)
        self.etype = rtype

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "+":
                self.value = self.left.get_value() + self.right.get_value()
            elif self.op == "-":
                self.value = self.left.get_value() - self.right.get_value()

    def generate_body(self, env):
        s = super(EAdd, self).generate_body(env)
        if self.etype == Type("string"):
            cFun = "concatenateString"
            s += "invokestatic " + env.get_fun_class(cFun) + "." + cFun \
                 + env.get_fun_type(cFun).generate_code_jvm() + "\n"
        elif self.op == "+":
            s += "iadd \n"
        else:
            s += "isub \n"
        env.pop_stack(1)
        return s


class EAnd(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EAnd, self).__init__(left, right, "&&", Type("boolean"), Type("boolean"), no_line,
                                   pos)
        self.type = "eand"
        self.label_pattern = "and_" + str(self.no_line) + "_" + str(self.pos)

    def calculate_value(self):
        if self.left.get_value() is False and self.left.get_value() is None:
            self.value = self.left.get_value()
        else:
            self.value = self.right.get_value()

    def generate_body(self, env):
        s = self.left.generate_code_jvm(env)
        s += "dup\n"
        s += "ifeq " + self.label_pattern + "\n"
        s += self.right.generate_code_jvm(env)
        s += "iand \n"
        s += self.label_pattern + ":\n"
        env.pop_stack(1)
        return s


class EApp(ZeroArgExpr):
    def __init__(self, funident, exprlist, no_line, pos):
        super(EApp, self).__init__(None, None, no_line, pos)
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist
        self.etype = None

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_function(self.funident):
                raise NotDeclaredException(self.funident, True, self.no_line, self.pos)
            self.etype = env.get_fun_type(self.funident)
            self.check_arg_list(env)

        return self.etype.return_type

    def check_arg_list(self, env):
        if len(self.exprlist) != len(self.etype.params_types):
            raise SyntaxException("Wrong number of parameters for function "
                                  + self.funident + " - expected:"
                                  + str(len(self.etype.params_types)) + " actual: "
                                  + str(len(self.exprlist)) + ".", self.no_line, pos=self.pos)

        for i in range(len(self.exprlist)):
            self.exprlist[i].type_check(env, self.etype.params_types[i])

    def generate_body(self, env):
        s = ""
        for expr in self.exprlist:
            s += expr.generate_code_jvm(env)
        s += "invokestatic " + env.get_fun_class(self.funident) + "." + self.funident + self.etype.generate_code_jvm()
        s += "\n"
        return s


class ELitBoolean(ZeroArgExpr):
    def __init__(self, lit, no_line, pos):
        super(ELitBoolean, self).__init__(True if lit == "true" else False, Type("boolean"), no_line, pos)
        self.type = "elitboolean"

    def generate_body(self, env):
        env.push_stack(1)
        return "iconst_1\n" if self.value else "iconst_0\n"


class ELitNull(ZeroArgExpr):
    def __init__(self, type, no_line, pos):
        #TODO: moze tu byc tablica jako type
        super(ELitNull, self).__init__(None, Type(type), no_line, pos)
        self.type = "elitnull"



class ELitInt(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(ELitInt, self).__init__(value, Type("int"), no_line, pos)
        self.type = "number"

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + str(self.value) + " \n"


class EObjectField(ZeroArgExpr):
    def __init__(self, obj, field, no_line, pos):
        super(EObjectField, self).__init__(None, None, no_line, pos)
        self.type = "objectfield"
        self.obj = obj
        self.field = field


class EObjectApp(ZeroArgExpr):
    def __init__(self, obj, method, no_line, pos):
        super(EObjectApp, self).__init__(None, None, no_line, pos)
        self.type = "objectapp"
        self.obj = obj
        self.method = method

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + str(self.value) + " \n"


class EMul(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EMul, self).__init__(left, right, op, Type("int"), Type("int"), no_line, pos)
        self.type = "emul"

    def calculate_value(self):
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "/":
                if self.right.get_value() == 0:
                    raise SyntaxException("Division by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() / self.right.get_value()
            elif self.op == "*":
                self.value = self.left.get_value() * self.right.get_value()
            elif self.op == "%":
                if self.right.get_value() == 0:
                    raise SyntaxException("Modulo by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() % self.right.get_value()

    def generate_body(self, env):
        s = super(EMul, self).generate_body(env)
        if self.op == "/":
            s += "idiv\n"
        elif self.op == "*":
            s += "imul\n"
        else:
            s += "irem\n"
        env.pop_stack(2)
        return s


class ENeg(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENeg, self).__init__(expr, Type("int"), no_line, pos)
        self.type = "eneg"

    def generate_body(self, env):
        s = super(ENeg, self).generate_body(env)
        s += "ineg\n"
        return s


class ENot(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENot, self).__init__(expr, Type("boolean"), no_line, pos)
        self.type = "enot"

    def generate_body(self, env):
        s = super(ENot, self).generate_body(env)
        env.push_stack(1)
        s += "iconst_1\n"
        s += "ixor\n"
        env.pop_stack(1)
        return s


class EOr(TwoArgExpr):
    def __init__(self, left, right, no_line, pos):
        super(EOr, self).__init__(left, right, "||", Type("boolean"), Type("boolean"), no_line,
                                  pos)
        self.type = "eor"
        self.label_pattern = "or_" + str(self.no_line) + "_" + str(self.pos)

    def calculate_value(self):
        if self.left.get_value() is True:
            self.value = True
        else:
            self.value = self.right.get_value()

    def generate_body(self, env):
        s = self.left.generate_code_jvm(env)
        s += "dup\n"
        env.push_stack(1)
        s += "ifne " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.right.generate_code_jvm(env)
        s += "ior \n"
        env.pop_stack(1)
        s += self.label_pattern + ":\n"
        return s


class ERel(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(ERel, self).__init__(left, right, op, Type("boolean"), None, no_line, pos)
        self.type = "erel"
        self.label_pattern = "cmp_" + str(self.no_line) + "_" + str(self.pos)

    def arg_type_check(self, rtype):
        if rtype == Type("boolean") and self.op != "==" and self.op != "!=":
            raise SyntaxException("Boolean does not support rel operators except '==' and '!='.",
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

    def generate_body(self, env):
        s = super(ERel, self).generate_body(env)
        if self.op == "==":
            s += "if_icmpeq"
        elif self.op == "!=":
            s += "if_icmpne"
        elif self.op == "<=":
            s += "if_icmple"
        elif self.op == ">=":
            s += "if_icmpge"
        elif self.op == "<":
            s += "if_icmplt"
        elif self.op == ">":
            s += "if_icmpgt"

        s += " "
        s += self.label_pattern + "_t\n"
        s += "goto " + self.label_pattern + "_f\n"

        s += self.label_pattern + "_t:\n"
        s += "iconst_1 \n"
        s += "goto " + self.label_pattern + "\n"

        s += self.label_pattern + "_f:\n"
        s += "iconst_0 \n"
        s += self.label_pattern + ":\n"
        return s


class EString(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(EString, self).__init__(value, Type("string"), no_line, pos)
        self.type = "estring"

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + self.value + " \n"


class EVar(ZeroArgExpr):
    def __init__(self, ident, no_line, pos):
        super(EVar, self).__init__(ident, None, no_line, pos)
        self.type = "var"

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                raise NotDeclaredException(self.value, False, self.no_line, self.pos)
            self.etype = env.get_variable_type(self.value)
        return self.etype

    def get_value(self):
        return None

    def generate_body(self, env):
        env.push_stack(1)
        if self.etype == Type("string"):
            return "aload " + str(env.get_variable_value(self.value)) + "\n"
        else:
            return "iload " + str(env.get_variable_value(self.value)) + "\n"


class EArrayInit(ZeroArgExpr):
    def __init__(self, type, array_length, no_line, pos):
        super(EArrayInit, self).__init__(None, ArrayType(type, array_length), no_line, pos)

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                raise NotDeclaredException(self.value, False, self.no_line, self.pos)
            self.etype = env.get_variable_type(self.value)
        return self.etype


class EArrayApp(ZeroArgExpr):
    def __init__(self, ident, index, no_line, pos):
        super(EArrayApp, self).__init__(ident, None, no_line, pos)
        self.index = index


class EObjectInit(ZeroArgExpr):
    def __init__(self, class_name, no_line, pos):
        super(EObjectInit, self).__init__(None, ClassType(class_name), no_line, pos)

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                raise NotDeclaredException(self.value, False, self.no_line, self.pos)
            self.etype = env.get_variable_type(self.value)
        return self.etype