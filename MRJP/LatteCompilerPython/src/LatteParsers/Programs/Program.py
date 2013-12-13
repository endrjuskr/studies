__author__ = 'Andrzej Skrodzki - as292510'

from Env import Env
from LatteExceptions import *
from LatteParsers.BaseNode import BaseNode
from ReadStringFun import ReadStringFun
from ReadIntFun import ReadIntFun
from ErrorFun import ErrorFun
from PrintStringFun import PrintStringFun
from PrintIntFun import PrintIntFun

class Program(BaseNode):
    def __init__(self, topdeflist):
        super(Program, self).__init__("program", -1, 0)
        self.topdeflist = topdeflist
        self.topdeflist.append(ErrorFun())
        self.topdeflist.append(ReadIntFun())
        self.topdeflist.append(ReadStringFun())
        self.topdeflist.append(PrintStringFun())
        self.topdeflist.append(PrintIntFun())

    def type_check(self):
        for fndef in self.topdeflist:
            self.env.add_fun(fndef)

        if not self.env.contain_main():
            raise SyntaxException.SyntaxException("Main funtion is not declared.", self.noline)

        for fndef in self.topdeflist:
            self.fun_check(fndef)


    def fun_check(self, fun):
        env_prim = self.env.copy()
        fun.type_check(env_prim)


    def generate_code(self):
        s = self.generate_header()
        for fn in self.topdeflist:
            s += fn.generate_code()
        s += self.generate_footer()
        return s

    def generate_header(self):
        return ".class public " + self.classname + + " \
                .super java/lang/Object \
                .method public <init>()V \
                aload_0 \
                invokespecial java/lang/Object/<init>()V \
                return \
                .end method"