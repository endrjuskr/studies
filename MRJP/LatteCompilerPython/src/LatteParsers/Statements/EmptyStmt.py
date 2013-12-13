__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase


class EmptyStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(EmptyStmt, self).__init__("emptystmt", no_line, pos)
