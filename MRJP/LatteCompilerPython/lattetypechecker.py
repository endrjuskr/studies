__author__ = 'andrzejskrodzki'
from Env import Env
import LatteParsers


class TypeCheck:
    def __init__(self, program):
        self.env = Env()
        self.program = program
        assert self.program.type == "program"

    def full_check(self):
        for fndef in self.program.topdeflist:
            self.env.add_fun(fndef)

        if not self.env.contain_main():
            print "Main function doesn't exist."
            exit(-1)

        for fndef in self.program.topdeflist:
            self.fun_check(fndef)


    def fun_check(self, fun):
        env_prim = self.prepare_env(fun.arglist)
        env_prim.current_fun_type = fun.funtype
        fun.block.type_check(env_prim)
        if fun.funtype.returntype.type != "void":
            if not fun.block.return_check():
                print fun.ident + " does not have proper return statement."
                exit(-1)


    def prepare_env(self, arglist):
        new_env = self.env.copy()
        for arg in arglist:
            new_env.add_variable(arg.ident, arg.argtype, -1)
        return new_env