__author__ = 'andrzejskrodzki'
from Env import Env
import LatteParsers


class TypeCheck:
    def __init__(self, program):
        self.env = Env()
        self.program = program
        assert self.program is LatteParsers.programparser.Program

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
        fun.block.type_check(env_prim)
        if fun.funtype.returntype.type == "void":
            fun.block.return_check()


    def prepare_env(self, arglist):
        new_env = self.env.copy()
        for arg in arglist:
            new_env.add_variable(arg.ident, arg.type)
        return new_env