__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["Arg", "InitItem", "ItemBase", "NoInitItem", "Field", "exception_list_par"]

from .BaseNode import *
from .LatteTypes import *
from ..LatteExceptions import *

exception_list_par = []

class Arg(BaseNode):
    def __init__(self, type, ident, no_line, pos):
        super(Arg, self).__init__("arg", no_line, pos)
        self.argtype = type
        self.ident = ident

    def type_check(self, env):
        if self.argtype.get_type() == Type("void"):
            exception_list_par.append(SyntaxException("Cannot initialize void variable.", self.no_line, self.pos))


class Field(BaseNode):
    def __init__(self, type, ident, no_line, pos):
        super(Field, self).__init__("field", no_line, pos)
        self.field_type = type
        self.ident = ident


class ItemBase(BaseNode):
    def __init__(self, ident, no_line, pos, type):
        super(ItemBase, self).__init__(type, no_line, pos)
        self.ident = ident
        self.itemtype = Type("void")

    def type_check(self, env):
        pass


class InitItem(ItemBase):
    def __init__(self, ident, expr, no_line, pos):
        super(InitItem, self).__init__(ident, no_line, pos, "inititem")
        self.expr = expr

    def type_check(self, env):
        if self.itemtype.get_type() == Type("void"):
            exception_list_par.append(SyntaxException("Cannot initialize void variable.", self.no_line, self.pos))
        self.expr.type_check(env, expected_type=self.itemtype)

    def generate_body(self, env):
        s = self.expr.generate_body(env)
        env.add_variable(self.ident, self.itemtype, self.no_line, self.pos, fun_param=False)
        if self.itemtype == Type("string"):
            s += "astore " + str(env.get_variable_value([self.ident])) + "\n"
        else:
            s += "istore " + str(env.get_variable_value([self.ident])) + "\n"
        return s

    def generate_code_asm(self, env, get_value=True):
        s = self.expr.generate_code_asm(env, get_value)
        if self.itemtype.is_array():
            env.add_variable(self.ident, None, self.no_line, self.pos, fun_param=False)
        env.add_variable(self.ident, self.itemtype, self.no_line, self.pos, fun_param=False)
        return s


class NoInitItem(ItemBase):
    def __init__(self, ident, no_line, pos):
        super(NoInitItem, self).__init__(ident, no_line, pos, "noinititem")

    def type_check(self, env):
        if self.itemtype.get_type() == Type("void"):
            exception_list_par.append(SyntaxException("Cannot initialize void variable.", self.no_line, self.pos))

    def generate_body(self, env):
        s = ""
        env.add_variable(self.ident, self.itemtype, self.no_line, self.pos, fun_param=False)
        if self.itemtype == Type("string"):
            s += "ldc \"\" \n"
            s += "astore " + str(env.get_variable_value([self.ident])) + "\n"
        else:
            s += "iconst_0 \n"
            s += "istore " + str(env.get_variable_value([self.ident])) + "\n"

        return s

    def generate_code_asm(self, env, get_value=True):
        s = ""
        env.add_variable(self.ident, self.itemtype, self.no_line, self.pos, fun_param=False)
        if self.itemtype == Type("string"):
            s += "mov rax, qword [string_empty]\n"
            s += "push rax\n"
        else:
            s += "mov rax, 0\n"
            s += "push rax\n"
        return s