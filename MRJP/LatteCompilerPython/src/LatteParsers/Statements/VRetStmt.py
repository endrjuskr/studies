__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase
from LatteExceptions import *
from LatteParsers.Types import *


class VRetStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(VRetStmt, self).__init__("vretstmt", no_line, pos)

    def type_check(self, env):
        if env.current_fun_type.returntype != Type.Type("void"):
            raise SyntaxException.SyntaxException("Incorrect return type, expected not void.", self.no_line,
                                                  pos=self.pos)
