__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["Env", "exception_list_env"]

from .LatteExceptions import *
from .LatteParsers.LatteTypes import *

exception_list_env = []


class Env:
    def __init__(self, orig=None, reset_declarations=True, class_name="MyClass"):
        self.predefined_fun = ["readInt", "readString", "error", "printInt", "printString", "concatenateString"]
        self.stack_var_size = 8
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
            self.stack_shift = 0
            self.array_size = {}
        else:
            self.array_size = dict(orig.array_size)
            self.var_env = dict(orig.var_env)
            self.fun_env = dict(orig.fun_env)
            self.class_env = orig.class_env.copy()
            self.var_store = dict(orig.var_store)
            self.var_decl = [] if reset_declarations else list(orig.var_decl)
            self.variables_counter = orig.variables_counter
            self.max_variable_counter = 0 if len(self.var_store.values()) == 0 else max(self.var_store.values()) + 1
            self.current_fun_type = orig.current_fun_type
            self.current_stack_count = orig.current_stack_count
            self.max_stack_count = orig.current_stack_count
            self.in_main = orig.in_main
            self.class_name = orig.class_name
            self.string_dict = orig.string_dict.copy()
            self.stack_shift = orig.stack_shift

    def add_string(self, s):
        size = len(self.string_dict)
        label = "string_" + str(size)
        self.string_dict[label] = s
        return label

    def increment_stack(self):
        self.stack_shift += self.stack_var_size

    def decrement_stack(self):
        self.stack_shift -= self.stack_var_size

    def add_fun(self, fun):
        if fun.ident in self.fun_env:
            exception_list_env.append(DuplicateDeclarationException(fun.ident, True, fun.no_line, 0))
        self.fun_env[fun.ident] = fun.funtype

    def add_class(self, class_def):
        if class_def.ident in self.class_env:
            exception_list_env.append(DuplicateDeclarationException(class_def.ident, True, class_def.no_line, 0))
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

    def get_class(self, ident):
        if not ident in self.class_env:
            exception_list_env.append(SyntaxException("Class " + ident + " does not exist.", 0))
            return None
        return self.class_env[ident]

    def contain_main(self):
        return "main" in self.fun_env and self.fun_env["main"] == FunType(Type("int"), [])

    def get_fun_type(self, ident):
        assert not ident in self.var_env
        return self.fun_env[ident]

    def add_variable(self, ident, type, no_line, pos, fun_param=True):
        if type is None:
            self.array_size[ident] = self.variables_counter
            self.variables_counter += 1
            return
        if ident in self.fun_env:
            exception_list_env.append(SyntaxException("Trying override function " + ident + ".", no_line))
        elif not ident in self.var_decl:
            self.var_env[ident] = type
            self.var_store[ident] = self.variables_counter
            self.var_decl.append(ident)
            self.variables_counter += 1
        elif fun_param:
            exception_list_env.append(SyntaxException("More than one argument with the name " + ident +
                                  ".", no_line, pos=pos))
        else:
            exception_list_env.append(DuplicateDeclarationException(ident, False, no_line, pos))

    def get_variable_type(self, ident):
        if not ident[0] in self.var_env:
            return None
        assert not ident[0] in self.fun_env
        t = self.var_env[ident[0]]
        for ide in ident[1:]:
            t = self.get_field_type(t.type, ide)
            if t is None:
                return None
        return t

    def get_array_type(self, ident):
        t = self.get_variable_type(ident)
        if t is not None:
            t = t.array_type
        return t

    def get_method_type(self, ident, method):
        return self.class_env[ident].get_method_type(method)

    def get_field_type(self, ident, field):
        t = self.class_env[ident].get_field_type(field)
        if t.is_fun():
            t = t.return_type
        if t.is_array():
            t = t.array_type
        return t

    def get_variable_value(self, ident):
        if len(ident) > 1:
            return None
        return self.var_store[ident[0]]

    def get_variable_position(self, ident):
        assert not ident in self.fun_env
        return (self.variables_counter - 1 - self.var_store[ident]) * self.stack_var_size + self.stack_shift

    def get_field_position(self, obj, field):
        return self.class_env[obj].get_field_position(field) * 8

    def get_array_length(self, ident):
        return (self.variables_counter - 1 - self.array_size[ident]) * self.stack_var_size + self.stack_shift

    def is_array(self, ident):
        return ident in self.array_size.keys()

    def get_struct_size(self, ident):
        return self.class_env[ident].get_size() * 8

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

    def check_types(self, type1, type2):
        if type1.is_simple() or type2.is_simple():
            return type1 == type2
        if type1 == type2:
            return True
        cl = self.class_env[type2.type]
        while len(cl.extlist) > 0:
            cl = self.class_env[cl.extlist[0]]
            if type1.type == cl.ident:
                return True
        return False