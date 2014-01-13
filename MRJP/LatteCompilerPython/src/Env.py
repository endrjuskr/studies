__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["Env"]

from .LatteExceptions import *
from .LatteParsers.LatteTypes import *


class Env:
    def __init__(self, orig=None, reset_declarations=True, class_name="MyClass"):
        self.predefined_fun = ["readInt", "readString", "error", "printInt", "printString", "concatenateString"]
        self.stack_shift = 0
        if orig is None:
            self.class_name = class_name
            self.current_fun_type = None
            self.current_stack_count = 0
            self.in_main = False
            self.var_env = {}
            self.class_env = {}
            self.fun_env = {}
            self.var_store = {}
            self.variables_counter = 0
            self.max_variable_counter = 0
            self.var_decl = []
            self.string_dict = {}
        else:
            self.var_env = orig.var_env.copy()
            self.fun_env = orig.fun_env.copy()
            self.class_env = orig.class_env.copy()
            self.var_store = orig.var_store.copy()
            self.var_decl = [] if reset_declarations else list(orig.var_decl)
            self.variables_counter = orig.variables_counter
            self.max_variable_counter = 0 if len(self.var_store.values()) == 0 else max(self.var_store.values()) + 1
            self.current_fun_type = orig.current_fun_type
            self.current_stack_count = orig.current_stack_count
            self.max_stack_count = orig.current_stack_count
            self.in_main = orig.in_main
            self.class_name = orig.class_name
            self.string_dict = orig.string_dict.copy()

    def add_string(self, s):
        size = len(self.string_dict)
        label = "string_" + str(size)
        self.string_dict[label] = s
        return label

    def increment_stack(self):
        self.stack_shift += 4

    def decrement_stack(self):
        self.stack_shift -= 4

    def add_fun(self, fun):
        if fun.ident in self.fun_env:
            raise DuplicateDeclarationException(fun.ident, True, fun.no_line, 0)
        self.fun_env[fun.ident] = fun.funtype

    def add_class(self, class_def):
        if class_def.ident in self.class_env:
            raise DuplicateDeclarationException(class_def.ident, True, class_def.no_line, 0)
        self.class_env[class_def.ident] = class_def

    def push_stack(self, number):
        self.current_stack_count += number
        self.max_stack_count = max(self.current_stack_count, self.max_stack_count)

    def pop_stack(self, number):
        self.current_stack_count -= number

    def contain_function(self, ident):
        return ident in self.fun_env

    def contain_variable(self, ident):
        return ident in self.var_env

    def contain_class(self, ident):
        return ident in self.class_env

    def contain_field(self, ident, field):
        return ident in self.class_env and self.class_env[ident].contain_field(field)

    def contain_method(self, ident, method):
        return ident in self.class_env and self.class_env[ident].contain_method(method)

    def contain_main(self):
        return "main" in self.fun_env and self.fun_env["main"] == FunType(Type("int"), [])

    def get_fun_type(self, ident):
        assert not ident in self.var_env
        return self.fun_env[ident]

    def add_variable(self, ident, type, no_line, pos, fun_param=True):
        if ident in self.fun_env:
            raise SyntaxException("Trying override function " + ident + ".", no_line)
        elif not ident in self.var_decl:
            self.var_env[ident] = type
            self.var_store[ident] = self.variables_counter
            self.var_decl.append(ident)
            self.variables_counter += 1
        elif fun_param:
            raise SyntaxException("More than one argument with the name " + ident
                                  + ".", no_line, pos=pos)
        else:
            raise DuplicateDeclarationException(ident, False, no_line, pos)

    def get_variable_type(self, ident):
        assert not ident in self.fun_env
        return self.var_env[ident]

    def get_array_type(self, ident):
        assert not ident in self.fun_env
        return None if not self.var_env[ident].is_array() else self.var_env[ident].get_type()

    def get_method_type(self, ident, method):
        return self.class_env[ident].get_method_type(method)

    def get_field_type(self, ident, field):
        assert not ident in self.fun_env
        return self.class_env[ident].get_field_type(field)

    def get_variable_value(self, ident):
        assert not ident in self.fun_env
        return self.var_store[ident]

    def get_variable_position(self, ident):
        assert not ident in self.fun_env
        return (max(self.var_store.values()) - self.var_store[ident] + 1) * 4 + self.stack_shift

    def get_fun_class(self, ident):
        if ident in self.predefined_fun:
            return "Runtime"
        else:
            return self.class_name

    def get_stack_limit(self):
        return self.max_stack_count

    def get_local_limit(self):
        return max(self.variables_counter, self.max_variable_counter)

    def __str__(self):
        output = ""
        for key, value in self.var_env.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        for key, value in self.fun_env.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        for key, value in self.var_store.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        return output

    def get_id_asm(self):
        pass