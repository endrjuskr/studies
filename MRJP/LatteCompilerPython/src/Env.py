__author__ = 'andrzejskrodzki'

from LatteParsers.typeparser import Type, FunType
from LatteExceptions import DuplicateDeclarationException, SyntaxException


class Env:
    current_env = {}
    current_fun_type = None

    def __init__(self, new_env={}, inside_fun=None):
        self.current_env = new_env
        self.current_fun_type = inside_fun
        if len(self.current_env) == 0:
            self.add_predifined_methods()

    def add_predifined_methods(self):
        self.current_env["printInt"] = FunType(Type("void"), [Type("int")])
        self.current_env["readInt"] = FunType(Type("int"), [])
        self.current_env["printString"] = FunType(Type("void"), [Type("string")])
        self.current_env["readString"] = FunType(Type("string"), [])
        self.current_env["error"] = FunType(Type("void"), [])

    def add_fun(self, fun):
        if self.current_env.has_key(fun.ident) and self.current_env[fun.ident] == fun.funtype:
            raise DuplicateDeclarationException.DuplicateDeclarationException(fun.ident, True, fun.no_line, 0)
        self.current_env[fun.ident] = fun.funtype

    def contain_funtion(self, ident):
        return self.current_env.has_key(ident) and hasattr(self.current_env[ident], "isFunction")

    def contain_variable(self, ident):
        return self.current_env.has_key(ident) and not hasattr(self.current_env[ident], "isFunction")


    def contain_main(self):
        return self.current_env.has_key("main") and self.current_env["main"] == FunType(Type("int"), [])

    def invoke_fun(self, ident):
        self.current_fun_type = self.current_env[ident]

    def get_fun_type(self, ident):
        assert hasattr(self.current_env[ident], "isFunction")
        return self.current_env[ident]

    def copy(self):
        new_env = {}
        for key, value in self.current_env.iteritems():
            if hasattr(value, "isFunction"):
                new_env[key] = value
            else:
                (t, _) = value
                new_env[key] = (t, 0)
        return Env(new_env=new_env, inside_fun=self.current_fun_type)

    def add_variable(self, ident, type, no_line, pos, fun_param=True):
        if not self.current_env.has_key(ident):
            self.current_env[ident] = (type, 0 if fun_param else 1)
        elif hasattr(self.current_env[ident], "isFunction"):
            raise SyntaxException.SyntaxException("Trying override function " + ident + ".", no_line)
        elif fun_param:
            raise SyntaxException.SyntaxException("More than one argument with the name " + ident
                                                 + " in function " + ident + ".", no_line)
        else:
            (_, count) = self.current_env[ident]
            if count > 0:
                raise DuplicateDeclarationException.DuplicateDeclarationException(ident, True, no_line, pos)
            else:
                self.current_env[ident] = (type, count + 1)

    def get_variable_type(self, ident):
        assert not hasattr(self.current_env[ident], "isFunction")
        return self.current_env[ident][0]

    def __str__(self):
        output = ""
        for key, value in self.current_env.iteritems():
            output += str(key) + " - " + str(value) + "\n"

        return output