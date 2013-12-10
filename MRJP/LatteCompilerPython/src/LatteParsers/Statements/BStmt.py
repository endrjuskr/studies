__author__ = 'andrzejskrodzki'

from StmtBase import StmtBase


class BStmt(StmtBase):
    def __init__(self, block, no_line):
        super(BStmt, self).__init__("blockstmt", no_line, 0)
        self.block = block

    def type_check(self, env):
        return self.block.type_check(env)

    def return_check(self):
        return self.block.return_check()