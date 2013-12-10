__author__ = 'andrzejskrodzki'

from TwoArgExpr import TwoArgExpr
from LatteParsers.Types import *
from LatteExceptions import *


class EMul(TwoArgExpr):
    def __init__(self, left, right, op, no_line, pos):
        super(EMul, self).__init__(left, right, op, Type.Type("int"), Type.Type("int"), no_line, pos)
        self.type = "emul"


    def calculate_value(self):
        #print self.op, self.right, self.left, self.no_line
        if self.left.get_value() is not None and self.right.get_value() is not None:
            if self.op == "/":
                if self.right.get_value() == 0:
                    raise SyntaxException.SyntaxException("Division by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() / self.right.get_value()
            elif self.op == "*":
                self.value = self.left.get_value() * self.right.get_value()
            elif self.op == "%":
                if self.right.get_value() == 0:
                    raise SyntaxException.SyntaxException("Modulo by 0", self.no_line, pos=self.pos)
                self.value = self.left.get_value() % self.right.get_value()

