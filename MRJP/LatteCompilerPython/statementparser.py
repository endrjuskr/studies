__author__ = 'andrzejskrodzki'


class Stmt:
    pass


class Block:
    def __init__(self, stmtlist):
        self.type = "block"
        self.stmtlist = stmtlist


class EmptyStmt(Stmt):
    def __init__(self):
        self.type = "emptystmt"


class BStmt(Stmt):
    def __init__(self, block):
        self.type = "blockstmt"
        self.block = block


class DeclStmt(Stmt):
    def __init__(self, itemtype, itemlist):
        self.type = "declstmt"
        self.itemtype = itemtype
        self.itemlist = itemlist
        self.settypes()

    def settypes(self):
        for item in self.itemlist:
            item.itemtype = self.itemtype


class Item:
    pass


class NoInitItem(Item):
    def __init__(self, ident):
        self.type = "noinititem"
        self.ident = ident
        self.itemtype = "unknown"


class InitItem(Item):
    def __init__(self, ident, expr):
        self.type = "inititem"
        self.ident = ident
        self.expr = expr


class AssStmt(Stmt):
    def __init__(self, ident, expr):
        self.type = "assstmt"
        self.ident = ident
        self.expr = expr


class IncrStmt(Stmt):
    def __init__(self, ident):
        self.type = "incrstmt"
        self.ident = ident


class DecrStmt(Stmt):
    def __init__(self, ident):
        self.type = "decrstmt"
        self.ident = ident


class RetStmt(Stmt):
    def __init__(self, expr):
        self.type = "retstmt"
        self.expr = expr


class VRetStmt(Stmt):
    def __init__(self):
        self.type = "vretstmt"


class CondStmt(Stmt):
    def __init__(self, expr, stmt):
        self.type = "condstmt"
        self.expr = expr
        self.stmt = stmt


class CondElseStmt(Stmt):
    def __init__(self, expr, stmt1, stmt2):
        self.type = "condelsestmt"
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2


class WhileStmt(Stmt):
    def __init__(self, expr, stmt):
        self.type = "whilestmt"
        self.expr = expr
        self.stmt = stmt


class SExpStmt(Stmt):
    def __init__(self, expr):
        self.type = "sexpstmt"
        self.expr = expr