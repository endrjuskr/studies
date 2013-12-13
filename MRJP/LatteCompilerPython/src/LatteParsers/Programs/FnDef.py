__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.Types.FunType import *
from Env import Env
from LatteExceptions import *
from LatteParsers.BaseNode import BaseNode

class FnDef(BaseNode):
    def __init__(self, type, ident, arglist, block, no_line):
        super(FnDef, self).__init__("fndef", no_line, 0)
        self.funtype = self.calculate_type(type, arglist)
        self.ident = ident
        self.arglist = arglist
        self.block = block

    def get_type(self, arg):
        return arg.argtype

    def type_check(self, env):
        self.prepare_env(env)
        env.current_fun_type = self.funtype
        self.block.type_check(env, reset_variables=False)
        if self.funtype.returntype.type != "void":
            if not self.block.return_check():
                raise ReturnException.ReturnException(self.ident, self.no_line)

    def prepare_env(self, env):
        for arg in self.arglist:
            env.add_variable(arg.ident, arg.argtype, arg.no_line, arg.pos)


    def calculate_type(self, type, arglist):
        return FunType(type, map(self.get_type, arglist))

    def generate_header(self):
        return ".method public static " + self.ident + self.funtype.generate_code()

    def generate_body(self):
        return ""

    def generate_footer(self):
        return ".end method"