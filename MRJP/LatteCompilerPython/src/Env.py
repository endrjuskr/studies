__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.Types import *
from LatteExceptions import DuplicateDeclarationException, SyntaxException


class Env:
    def __init__(self, orig=None):
        self.predefined_fun = ["readInt", "readString", "error", "printInt", "printString", "concatenateString"]
        if orig is None:
            self.var_env = {}
            self.fun_env = {}
            self.var_store = {}
            self.var_decl = []
            self.reg_env = {}
            self.variables_counter = 0
            self.max_variable_counter = 0
        else:
            self.var_env = orig.var_env
            self.fun_env = orig.fun_env
            self.var_store = orig.var_store
            self.var_decl = orig.var_decl
            self.reg_env = orig.reg_env
            self.variables_counter = orig.variables_counter
            self.max_variable_counter = 0 if len(self.var_store.values()) == 0 else max(self.var_store.values()) + 1
            self.current_fun_type = orig.current_fun_type
            self.current_stack_count = orig.current_stack_count
            self.max_stack_count = orig.current_stack_count
            self.in_main = orig.in_main
            self.class_name = orig.class_name

    def add_fun(self, fun):
        if fun.ident in self.fun_env:
            raise DuplicateDeclarationException.DuplicateDeclarationException(fun.ident, True, fun.no_line, 0)
        self.fun_env[fun.ident] = fun.funtype

    def push_stack(self, number):
        self.current_stack_count += number
        self.max_stack_count = max(self.current_stack_count, self.max_stack_count)

    def pop_stack(self, number):
        self.current_stack_count -= number

    def contain_function(self, ident):
        return ident in self.fun_env

    def contain_variable(self, ident):
        return ident in self.var_env

    def contain_main(self):
        return "main" in self.fun_env and self.fun_env["main"] == FunType.FunType(Type.Type("int"), [])

    def get_fun_type(self, ident):
        assert not ident in self.var_env
        return self.fun_env[ident]

    def shallow_copy(self):
        new_var_env = {}
        for key, value in self.var_env.iteritems():
            (t, _) = value
            # Resetting all variables' counters so they can be overwritten
            new_var_env[key] = (t, 0)

        new_var_env = map(lambda (t, _): (t,0 ), self.var_env)

        new_fun_env = self.fun_env.copy()
        new_var_store = self.var_store.copy()
        new_reg_env = self.reg_env.copy()

        return Env(var_env=new_var_env, fun_env=new_fun_env, var_store=new_var_store,
                   reg_env=new_reg_env, inside_fun=self.current_fun_type, in_main=self.in_main,
                   current_stack=self.current_stack_count, class_name=self.class_name)

    def deep_copy(self):
        new_var_env = {}
        for key, value in self.var_env.iteritems():
            new_var_env[key] = value

        new_fun_env = {}
        for key, value in self.fun_env.iteritems():
            new_fun_env[key] = value

        new_var_store = {}
        for key, value in self.var_store.iteritems():
            new_var_store[key] = value

        new_reg_env = {}
        for key, value in self.reg_env.iteritems():
            new_reg_env[key] = value

        return Env(var_env=new_var_env, fun_env=new_fun_env, var_store=new_var_store,
                   reg_env=new_reg_env, inside_fun=self.current_fun_type, in_main=self.in_main,
                   current_stack=self.current_stack_count, class_name=self.class_name)

    def add_variable(self, ident, type, no_line, pos, fun_param=True):
        if ident in self.fun_env:
            raise SyntaxException.SyntaxException("Trying override function " + ident + ".", no_line)
        elif not ident in self.var_env:
            self.var_env[ident] = (type, 1)
            self.var_store[ident] = self.variables_counter
            self.variables_counter += 1
        elif fun_param:
            raise SyntaxException.SyntaxException("More than one argument with the name " + ident +
                                                  ".", no_line, pos=pos)
        else:
            (_, count) = self.var_env[ident]
            if count > 0:
                raise DuplicateDeclarationException.DuplicateDeclarationException(ident, False, no_line, pos)
            else:
                self.var_env[ident] = (type, count + 1)
                self.var_store[ident] = self.variables_counter
                self.variables_counter += 1

    def get_variable_type(self, ident):
        assert not ident in self.fun_env
        return self.var_env[ident][0]

    def get_variable_value(self, ident):
        assert not ident in self.fun_env
        return self.var_store[ident]

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

