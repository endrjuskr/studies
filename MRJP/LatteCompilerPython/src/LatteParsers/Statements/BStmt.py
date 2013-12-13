__author__ = 'Andrzej Skrodzki - as292510'

from StmtBase import StmtBase


class BStmt(StmtBase):
    def __init__(self, block, no_line):
        super(BStmt, self).__init__("blockstmt", no_line, 0)
        self.block = block

    def type_check(self, env):
        self.block.type_check(env)

    def return_check(self):
        return self.block.return_check()

    def generate_body(self, env):
        env_prim = env.shallow_copy()
        s = self.block.generate_code(env_prim)
        env.variables_counter = env_prim.variables_counter
        return s