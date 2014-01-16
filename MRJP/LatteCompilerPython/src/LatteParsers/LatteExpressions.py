__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["EAdd", "EAnd", "EApp", "ELitBoolean", "ELitInt", "EMul", "ENeg", "ENot", "EOr", "ERel", "EString", "EVar",
           "ExprBase", "OneArgExpr", "TwoArgExpr", "ZeroArgExpr", "EArrayInit", "EArrayApp", "EObjectInit",
           "ELitNull", "EObjectField", "EObjectApp", "exception_list_expr"]

from .BaseNode import *
from ..LatteExceptions import *
from .LatteTypes import *

exception_list_expr = []


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
            exception_list_expr.append(TypeException(expected_type, self.etype, self.no_line, self.pos))
        self.expr.type_check(env, self.etype)
        return self.etype

    def calculate_value(self):
        if self.expr.value is not None:
            self.value = - self.expr.value

    def generate_body(self, env):
        return self.expr.generate_code_jvm(env)

    def generate_code_asm(self, env):
        s = self.expr.generate_code_asm(env)
        s += "pop rax\n"
        return s


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

        error_occured = False
        if expected_type is not None and self.etype is not None and expected_type != self.etype:
            exception_list_expr.append(TypeException(expected_type, self.etype, self.no_line, self.pos))
            error_occured = True
        if expected_type is not None and self.etype is None and expected_type != rtype:
            exception_list_expr.append(TypeException(expected_type, rtype, self.no_line, self.pos))
            error_occured = True

        if not error_occured:
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
        env.increment_stack()
        s += self.right.generate_code_asm(env)
        env.decrement_stack()
        s += "pop rbx\n"
        s += "pop rax\n"
        return s


class ZeroArgExpr(ExprBase):
    def __init__(self, value, etype, no_line, pos):
        super(ZeroArgExpr, self).__init__(etype, no_line, pos)
        self.value = value

    def type_check(self, env, expected_type=None):
        if expected_type is not None and expected_type != self.get_type(env):
            exception_list_expr.append(TypeException(expected_type, self.get_type(env), self.no_line, self.pos))
            return expected_type

        return self.get_type(env)

    def get_type(self, env):
        return self.etype


class EAdd(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EAdd, self).__init__(left, right, op, None, None, no_line, pos)
        self.type = "eadd"

    def arg_type_check(self, rtype):
        if rtype == Type("boolean"):
            exception_list_expr.append(SyntaxException("Boolean does not support add operators.", self.no_line, pos=self.pos))
        if rtype == Type("string") and self.op == "-":
            exception_list_expr.append(SyntaxException("String does not support - operator.", self.no_line, pos=self.pos))
        self.etype = rtype

    def calculate_value(self):
        try:
            if self.left.get_value() is not None and self.right.get_value() is not None:
                if self.op == "+":
                    self.value = self.left.get_value() + self.right.get_value()
                elif self.op == "-":
                    self.value = self.left.get_value() - self.right.get_value()
        except TypeError:
            self.value = None

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

    def generate_code_asm(self, env):
        s = super(EAdd, self).generate_code_asm(env)
        if self.etype == Type("string"):
            s += "mov rdi, rax\n"
            s += "mov rsi, rbx\n"
            s += "call contactString\n"
        elif self.op == "+":
            s += "add rax, rbx\n"
        else:
            s += "sub rax, rbx\n"
        s += "push rax\n"
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

    def generate_code_asm(self, env):
        s = self.left.generate_code_asm(env)
        s += "mov rax, [rsp]\n"
        s += "cmp rax, 0\n"
        s += "je " + self.label_pattern + "\n"
        env.increment_stack()
        s += self.right.generate_code_asm(env)
        env.decrement_stack()
        s += "pop rbx\n"
        s += "pop rax\n"
        s += "and rax, rbx \n"
        s += "push rax\n"
        s += self.label_pattern + ":\n"
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
                exception_list_expr.append(NotDeclaredException(self.funident, True, self.no_line, self.pos))
                return Type("void")
            else:
                self.etype = env.get_fun_type(self.funident)
                self.check_arg_list(env)

        return self.etype.return_type

    def check_arg_list(self, env):
        if len(self.exprlist) != len(self.etype.params_types):
            exception_list_expr.append(SyntaxException("Wrong number of parameters for function "
                                  + self.funident + " - expected:"
                                  + str(len(self.etype.params_types)) + " actual: "
                                  + str(len(self.exprlist)) + ".", self.no_line, pos=self.pos))

        for i in range(min(len(self.exprlist), len(self.etype.params_types))):
            self.exprlist[i].type_check(env, self.etype.params_types[i])

    def generate_body(self, env):
        s = ""
        for expr in self.exprlist:
            s += expr.generate_code_jvm(env)
        s += "invokestatic " + env.get_fun_class(self.funident) + "." + self.funident + self.etype.generate_code_jvm()
        s += "\n"
        return s

    def generate_code_asm(self, env):
        s = ""
        shift = 0
        for expr in self.exprlist:
            s += expr.generate_code_asm(env)
            if self.funident in env.predefined_fun:
                s += "pop rdi\n"
                pass
            else:
                if expr.etype.is_array():
                    env.increment_stack()
                    shift += 8
                env.increment_stack()
                shift += 8
        s += "call " + self.funident + "\n"
        if not self.funident in env.predefined_fun:
            env.stack_shift -= shift
            s += "add rsp, " + str(shift) + "\n"
        if env.get_fun_type(self.funident).return_type != Type("void"):
            if env.get_fun_type(self.funident).return_type.is_array():
                s += "push rbx\n"
            s += "push rax\n"
        return s


class ELitBoolean(ZeroArgExpr):
    def __init__(self, lit, no_line, pos):
        super(ELitBoolean, self).__init__(True if lit == "true" else False, Type("boolean"), no_line, pos)
        self.type = "elitboolean"

    def generate_body(self, env):
        env.push_stack(1)
        return "iconst_1\n" if self.value else "iconst_0\n"

    def generate_code_asm(self, env):
        s = "mov rax, " + ("1\n" if self.value else "0\n")
        s += "push rax\n"
        return s


class ELitNull(ZeroArgExpr):
    def __init__(self, type, no_line, pos):
        super(ELitNull, self).__init__(None, Type(type), no_line, pos)
        self.type = "elitnull"


class ELitInt(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(ELitInt, self).__init__(value, Type("int"), no_line, pos)
        self.type = "number"

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + str(self.value) + " \n"

    def generate_code_asm(self, env):
        s = "mov rax, " + str(self.value) + "\n"
        s += "push rax\n"
        return s


class EObjectField(ZeroArgExpr):
    def __init__(self, obj, field, no_line, pos):
        super(EObjectField, self).__init__(None, None, no_line, pos)
        self.type = "objectfield"
        self.obj = obj
        self.field = field

    def get_type(self, env):
        if not env.contain_variable(self.obj):
            exception_list_expr.append(NotDeclaredException(self.obj, False, self.no_line, self.pos))
        object_type = env.get_variable_type(self.obj)
        if object_type.is_array():
            if self.field != "length":
                exception_list_expr.append(NotDeclaredException("array." + self.field, True, self.no_line, self.pos))
            return Type("int")

        if not env.contain_class(object_type.type):
            exception_list_expr.append(BaseException(self.obj + " is not an object"))

        field_type = env.get_field_type(object_type.type, self.field)
        if field_type is None:
            exception_list_expr.append(BaseException(object_type + "." + self.field + " does not exist"))
        return field_type

    def generate_code_asm(self, env):
        position = env.get_array_length(self.obj)
        s = "mov rax, [rsp + " + str(position) + "]\n"
        s += "push rax\n"
        return s


class EObjectApp(ZeroArgExpr):
    def __init__(self, object_name, method_name, exprlist, no_line, pos):
        super(EObjectApp, self).__init__(None, None, no_line, pos)
        self.type = "objectapp"
        self.object_name = object_name
        self.method_name = method_name
        self.exprlist = exprlist
        self.object_class = None

    def get_type(self, env):
        if not env.contain_variable(self.object_name):
            exception_list_expr.append(NotDeclaredException(self.object_name, True, self.no_line, self.pos))
        self.object_class = env.get_variable_type()
        if not env.contain_class(self.object_class.type):
            exception_list_expr.append(Exception("There is no class called " + self.object_class.type))
        if not env.contain_method(self.object_class.type, self.method_name):
            exception_list_expr.append(NotDeclaredException(self.object_class.type + "." + self.method_name, True, self.no_line, self.pos))
        self.etype = env.get_method_type(self.object_class.type, self.method_name)
        self.check_arg_list(env)

    def check_arg_list(self, env):
        if len(self.exprlist) != len(self.etype.params_types):
            exception_list_expr.append(SyntaxException("Wrong number of parameters for function "
                                  + self.object_class.type + "." + self.method_name + " - expected:"
                                  + str(len(self.etype.params_types)) + " actual: "
                                  + str(len(self.exprlist)) + ".", self.no_line, pos=self.pos))

        for i in range(len(self.exprlist)):
            self.exprlist[i].type_check(env, self.etype.params_types[i])


class EMul(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EMul, self).__init__(left, right, op, Type("int"), Type("int"), no_line, pos)
        self.type = "emul"

    def calculate_value(self):
        try:
            if self.left.get_value() is not None and self.right.get_value() is not None:
                if self.op == "/":
                    if self.right.get_value() == 0:
                        exception_list_expr.append(SyntaxException("Division by 0", self.no_line, pos=self.pos))
                    self.value = self.left.get_value() / self.right.get_value()
                elif self.op == "*":
                    self.value = self.left.get_value() * self.right.get_value()
                elif self.op == "%":
                    if self.right.get_value() == 0:
                        exception_list_expr.append(SyntaxException("Modulo by 0", self.no_line, pos=self.pos))
                    self.value = self.left.get_value() % self.right.get_value()
        except TypeError:
            self.value = None
        except ZeroDivisionError:
            self.value = None

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

    def generate_code_asm(self, env):
        s = super(EMul, self).generate_code_asm(env)
        s += "mov rdx, 0\n" # wyzerowac
        if self.op == "/":
            s += "idiv rbx\n"
        elif self.op == "*":
            s += "imul rax, rbx\n"
        else:
            s += "idiv rbx\n"
            s += "mov rax, rdx\n"
        s += "push rax\n"
        return s


class ENeg(OneArgExpr):
    def __init__(self, expr, no_line, pos):
        super(ENeg, self).__init__(expr, Type("int"), no_line, pos)
        self.type = "eneg"

    def generate_body(self, env):
        s = super(ENeg, self).generate_body(env)
        s += "ineg\n"
        return s

    def generate_code_asm(self, env):
        s = super(ENeg, self).generate_code_asm(env)
        s += "neg rax\n"
        s += "push rax\n"
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

    def generate_code_asm(self, env):
        s = super(ENot, self).generate_code_asm(env)
        s += "xor rax, 1\n"
        s += "push rax\n"
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

    def generate_code_asm(self, env):
        s = self.left.generate_code_asm(env)
        s += "mov rax, [rsp]\n"
        s += "cmp rax, 1\n"
        s += "je " + self.label_pattern + "\n"
        env.increment_stack()
        s += self.right.generate_code_asm(env)
        env.decrement_stack()
        s += "pop rbx\n"
        s += "pop rax\n"
        s += "or rax, rbx \n"
        s += "push rax\n"
        s += self.label_pattern + ":\n"
        return s


class ERel(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(ERel, self).__init__(left, right, op, Type("boolean"), None, no_line, pos)
        self.type = "erel"
        self.label_pattern = "cmp_" + str(self.no_line) + "_" + str(self.pos)

    def arg_type_check(self, rtype):
        if rtype == Type("boolean") and self.op != "==" and self.op != "!=":
            exception_list_expr.append(SyntaxException("Boolean does not support rel operators except '==' and '!='.",
                                  self.no_line, pos=self.pos))

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

    def generate_code_asm(self, env):
        s = super(ERel, self).generate_code_asm(env)
        s += "cmp rax, rbx\n"
        if self.op == "==":
            s += "je"
        elif self.op == "!=":
            s += "jne"
        elif self.op == "<=":
            s += "jle"
        elif self.op == ">=":
            s += "jge"
        elif self.op == "<":
            s += "jl"
        elif self.op == ">":
            s += "jg"

        s += " "
        s += self.label_pattern + "_t\n"
        s += "jmp " + self.label_pattern + "_f\n"

        s += self.label_pattern + "_t:\n"
        s += "mov rax, 1\n"
        s += "jmp " + self.label_pattern + "\n"

        s += self.label_pattern + "_f:\n"
        s += "mov rax, 0\n"
        s += self.label_pattern + ":\n"
        s += "push rax\n"
        return s


class EString(ZeroArgExpr):
    def __init__(self, value, no_line, pos):
        super(EString, self).__init__(value, Type("string"), no_line, pos)
        self.type = "estring"

    def generate_body(self, env):
        env.push_stack(1)
        return "ldc " + self.value + "\n"

    def generate_code_asm(self, env):
        label = env.add_string(self.value)
        s = "mov rax, " + label + "\n"
        s += "push rax\n"
        return s


class EVar(ZeroArgExpr):
    def __init__(self, ident, no_line, pos):
        super(EVar, self).__init__(ident, None, no_line, pos)
        self.type = "var"

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_variable(self.value):
                exception_list_expr.append(NotDeclaredException(self.value, False, self.no_line, self.pos))
                return Type("void")
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

    def generate_code_asm(self, env):
        s = ""
        if env.is_array(self.value):
            position = env.get_array_length(self.value)
            s += "mov rax, [rsp + " + str(position) + "]\n"
            s += "push rax\n"
            env.increment_stack()
        s += "mov rax, [rsp + " + str(env.get_variable_position(self.value)) + "]\n"
        s += "push rax\n"
        if env.is_array(self.value):
            env.decrement_stack()
        return s


class EArrayInit(ZeroArgExpr):
    def __init__(self, type, array_length, no_line, pos):
        super(EArrayInit, self).__init__(None, ArrayType(type), no_line, pos)
        self.array_length = array_length
        self.a_type = type

    def get_type(self, env):
        self.array_length.type_check(env, expected_type=Type("int"))
        return self.etype

    def generate_code_asm(self, env):
        s = self.array_length.generate_code_asm(env)
        s += "mov rdi, [rsp]\n"
        if self.a_type == Type("string"):
            s += "mov rsi, 1\n"
        else:
            s += "mov rsi, 8\n"
        s += "call calloc\n"
        s += "push rax\n"
        return s



class EArrayApp(ZeroArgExpr):
    def __init__(self, ident, index, no_line, pos):
        super(EArrayApp, self).__init__(ident, None, no_line, pos)
        self.index = index

    def get_type(self, env):
        if not env.contain_variable(self.value):
            exception_list_expr.append(NotDeclaredException(self.value, False, self.no_line, self.pos))
        self.index.type_check(env, expected_type=Type("int"))
        array_type = env.get_array_type(self.value)
        if array_type is None:
            exception_list_expr.append(BaseException(self.value + " is not an array."))
        return array_type

    def get_value(self):
        return None

    def generate_code_asm(self, env):
        s = self.index.generate_code_asm(env)
        s += "pop rbx\n"
        s += "shl rbx, 3\n" # * 8
        s += "mov rax, [rsp + " + str(env.get_variable_position(self.value)) + "]\n"
        s += "add rax, rbx\n"
        s += "push qword [rax]\n"
        return s

class EObjectInit(ZeroArgExpr):
    def __init__(self, class_type, no_line, pos):
        super(EObjectInit, self).__init__(None, class_type, no_line, pos)