__author__ = 'andrzejskrodzki'


class Block():
    def __init__(self, stmtlist):
        self.type = "block"
        self.stmtlist = stmtlist

    def type_check(self, env, should_copy=True):
        if should_copy:
            env_prim = env.copy()
        else:
            env_prim = env
        for stmt in self.stmtlist:
            env_prim = stmt.type_check(env_prim)
        return env

    def return_check(self):
        for i in range(len(self.stmtlist)):
            if self.stmtlist[i].return_check():
                return True
        return False