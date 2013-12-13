__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.Types import *
from LatteExceptions import DuplicateDeclarationException, SyntaxException


class Env:
    current_env = {}
    current_fun_type = None

    def __init__(self, var_env={}, fun_env={}, var_store={}, inside_fun=None):
        self.var_env = var_env
        self.fun_env = fun_env
        self.var_store = var_store
        self.variables_counter = max(self.var_store.values()) + 1
        self.current_fun_type = inside_fun

    def add_fun(self, fun):
        if fun.ident in self.fun_env:
            raise DuplicateDeclarationException.DuplicateDeclarationException(fun.ident, True, fun.no_line, 0)
        self.fun_env[fun.ident] = fun.funtype

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

        new_fun_env = {}
        for key, value in self.fun_env.iteritems():
            new_fun_env[key] = value

        new_var_store = {}
        for key, value in self.var_store.iteritems():
            new_var_store[key] = value

        return Env(var_env=new_var_env, fun_env=new_fun_env, var_store=new_var_store,
                   inside_fun=self.current_fun_type)

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

        return Env(var_env=new_var_env, fun_env=new_fun_env, var_store=new_var_store,
                   inside_fun=self.current_fun_type)

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
                self.variables_counter[ident] = self.variables_counter
                self.variables_counter += 1

    def get_variable_type(self, ident):
        assert not ident in self.fun_env
        return self.var_env[ident][0]

    def get_variable_value(self, ident):
        assert not ident in self.fun_env
        return self.var_store[ident]

    def __str__(self):
        output = ""
        for key, value in self.var_env.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        for key, value in self.fun_env.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        for key, value in self.var_store.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        return output