__author__ = 'andrzejskrodzki'

from ZeroArgExpr import ZeroArgExpr
from LatteExceptions import *


class EApp(ZeroArgExpr):
    def __init__(self, funident, exprlist, no_line, pos):
        super(EApp, self).__init__(None, None, no_line, pos)
        self.type = "eapp"
        self.funident = funident
        self.exprlist = exprlist

    def get_type(self, env):
        if self.etype is None:
            if not env.contain_funtion(self.funident):
                raise NotDeclaredException.NotDeclaredException(self.funident, True, self.no_line, self.pos)
            self.etype = env.get_fun_type(self.funident)
            self.check_arg_list(env)

        return self.etype.returntype

    def check_arg_list(self, env):
        if len(self.exprlist) != len(self.etype.paramstypes):
            raise SyntaxException.SyntaxException("Wrong number of parameters for function "
                                                  + self.funident + " - expected:"
                                                  + str(len(self.etype.paramstypes)) + " actual: "
                                                  + str(len(self.exprlist)) + ".", self.no_line, pos=self.pos)

        for i in range(len(self.exprlist)):
            #print "arg"
            self.exprlist[i].type_check(env, self.etype.paramstypes[i])