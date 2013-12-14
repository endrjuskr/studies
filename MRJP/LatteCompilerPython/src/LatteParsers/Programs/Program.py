__author__ = 'Andrzej Skrodzki - as292510'

from Env import Env
from LatteExceptions.SyntaxException import SyntaxException
from LatteParsers.BaseNode import BaseNode
from PredefinedFun import *

class Program(BaseNode):
    def __init__(self, topdeflist):
        super(Program, self).__init__("program", -1, 0)
        self.topdeflist = topdeflist
        self.topdeflist.append(ErrorFun())
        self.topdeflist.append(ReadIntFun())
        self.topdeflist.append(ReadStringFun())
        self.topdeflist.append(PrintStringFun())
        self.topdeflist.append(PrintIntFun())
        self.topdeflist.append(ConcatenateStringFun())
        self.classname = "MyClass"

    def type_check(self):
        env = Env()
        for fndef in self.topdeflist:
            env.add_fun(fndef)

        for fndef in self.topdeflist:
            self.fun_check(fndef, env)

        if env.contain_main() is False:
            raise SyntaxException("Main funtion is not declared.", self.no_line)


    def fun_check(self, fun, env):
        env_prim = env.shallow_copy()
        fun.type_check(env_prim)


    def generate_body(self, env):
        for fndef in self.topdeflist:
            env.add_fun(fndef)

        s = ""
        for fn in self.topdeflist:
            env_prim = env.shallow_copy()
            s += fn.generate_code(env_prim)
        return s

    def generate_header(self):
        return ".class public " + self.classname + \
                "\n.super java/lang/Object \n \
                .method public <init>()V \n \
                aload_0 \n \
                invokespecial java/lang/Object/<init>()V \n \
                return \n \
                .end method \n"