__author__ = 'andrzejskrodzki'

from StmtBase import StmtBase


class DeclStmt(StmtBase):
    def __init__(self, itemtype, itemlist, no_line, pos):
        super(DeclStmt, self).__init__("declstmt", no_line, pos)
        self.itemtype = itemtype
        self.itemlist = itemlist
        self.settypes()

    def settypes(self):
        for item in self.itemlist:
            item.itemtype = self.itemtype

    def type_check(self, env):
        for item in self.itemlist:
            item.type_check(env)
            env.add_variable(item.ident, item.itemtype, item.no_line, item.pos, fun_param=False)
        return env