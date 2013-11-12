__author__ = 'andrzejskrodzki'

from typeparser import Type, FunType


class Env:
    current_env = dict
    current_fun_type = None

    def __init__(self, new_env={}):
        self.current_env = new_env
        if self.current_env.__len__ == 0:
            self.add_predifined_methods()

    def add_predifined_methods(self):
        self.current_env["printInt"] = FunType(Type("void"), [Type("int")])
        self.current_env["readInt"] = FunType(Type("int"), [])
        self.current_env["printString"] = FunType(Type("void"), [Type("string")])
        self.current_env["readString"] = FunType(Type("string"), [])
        self.current_env["error"] = FunType(Type("void"), [])

    def add_fun(self, fun):
        if self.current_env[fun.ident] is not None and self.current_env[fun.ident] == fun.funtype:
            print "Function already exists with this name and type."
            exit(-1)
        self.current_env[fun.ident] = fun.funtype

    def contain_ident(self, ident):
        return self.current_env[ident] is not None

    def contain_main(self):
        return self.current_env["main"] is not None and self.current_env["main"] == FunType(Type("int"), [])

    def invoke_fun(self, ident):
        self.current_fun_type = self.current_env[ident]

    def get_fun_type(self, ident):
        assert self.current_env[ident] is FunType
        return self.current_env[ident]

    def get_var_type(self, ident):
        assert self.current_env[ident] is Type
        return self.current_env[ident]

    def copy(self):
        new_env = dict
        for key, value in self.current_env:
            new_env[key] = value
        return Env(new_env=new_env)

    def add_variable(self, ident, type, fun_param=True):
        if self.current_env[ident] is None:
            self.current_env[ident] = (type, 0 if fun_param else 1)
        elif self.current_env[ident] is FunType:
            print "Trying override function."
            exit(-1)
        elif fun_param:
            print "Two arguments with the same name."
            exit(-1)
        else:
            (_, count) = self.current_env[ident]
            if count > 0:
                print "Variable has been already declared in the block."
                exit(-1)
            else:
                self.current_env[ident] = (type, count + 1)

    def get_variable_type(self, ident):
        return None if self.current_env[ident] is None else self.current_env[ident][0]