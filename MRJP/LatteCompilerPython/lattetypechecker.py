__author__ = 'andrzejskrodzki'

from Env import Env
from LatteExceptions import ReturnException, SyntaxException


class TypeCheck:
    def __init__(self, program):
        self.env = Env()
        self.program = program
        assert self.program.type == "program"

    def full_check(self):
        for fndef in self.program.topdeflist:
            self.env.add_fun(fndef)

        if not self.env.contain_main():
            raise SyntaxException.SyntaxEception("Main funtion is not declared.", 0)

        for fndef in self.program.topdeflist:
            self.fun_check(fndef)


    def fun_check(self, fun):
        env_prim = self.prepare_env(fun.arglist)
        env_prim.current_fun_type = fun.funtype
        fun.block.type_check(env_prim)
        if fun.funtype.returntype.type != "void":
            if not fun.block.return_check():
                raise ReturnException.ReturnException(fun.ident, fun.no_line)


    def prepare_env(self, arglist):
        new_env = self.env.copy()
        for arg in arglist:
            new_env.add_variable(arg.ident, arg.argtype, arg.no_line, arg.pos)
        return new_env