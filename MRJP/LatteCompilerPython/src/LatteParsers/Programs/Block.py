__author__ = 'Andrzej Skrodzki - as292510'

from LatteParsers.BaseNode import BaseNode
from Env import Env

class Block(BaseNode):
    def __init__(self, stmt_list):
        super(Block, self).__init__("block", 0, 0)
        self.stmt_list = stmt_list
        self.env = Env()

    def type_check(self, env, reset_variables=True):
        if reset_variables:
            env_prim = env.shallow_copy()
        else:
            env_prim = env.deep_copy()
        for stmt in self.stmt_list:
            stmt.type_check(env_prim)
        self.env = env_prim

    def return_check(self):
        for i in range(len(self.stmt_list)):
            if self.stmtlist[i].return_check():
                return True
        return False