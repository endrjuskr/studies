__author__ = 'andrzejskrodzki'

import typeparser
from LatteExceptions import NotDeclaredException, SyntaxException

class Stmt:
    pass


class Block:
    def __init__(self, stmtlist):
        self.type = "block"
        self.stmtlist = stmtlist

    def type_check(self, env):
        env_prim = env.copy()
        for stmt in self.stmtlist:
            env_prim = stmt.type_check(env_prim)
        return env

    def return_check(self):
        for i in range(len(self.stmtlist)):
            if self.stmtlist[i].return_check():
                return True
        return False


class EmptyStmt(Stmt):
    def __init__(self):
        self.type = "emptystmt"

    def type_check(self, env):
        return env

    def return_check(self):
        return False


class BStmt(Stmt):
    def __init__(self, block):
        self.type = "blockstmt"
        self.block = block

    def type_check(self, env):
        return self.block.type_check(env)

    def return_check(self):
        return self.block.return_check()


class DeclStmt(Stmt):
    def __init__(self, itemtype, itemlist, no_line):
        self.type = "declstmt"
        self.itemtype = itemtype
        self.itemlist = itemlist
        self.no_line = no_line
        self.settypes()

    def settypes(self):
        for item in self.itemlist:
            item.itemtype = self.itemtype

    def type_check(self, env):
        for item in self.itemlist:
            item.type_check(env)
            env.add_variable(item.ident, item.itemtype, item.no_line, item.pos, fun_param=False)
        return env

    def return_check(self):
        return False


class Item:
    pass


class NoInitItem(Item):
    def __init__(self, ident, no_line, pos):
        self.type = "noinititem"
        self.ident = ident
        self.itemtype = "unknown"
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        pass


class InitItem(Item):
    def __init__(self, ident, expr, no_line, pos):
        self.type = "inititem"
        self.ident = ident
        self.expr = expr
        self.itemtype = "unknown"
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        self.expr.type_check(env, expected_type=self.itemtype)


class AssStmt(Stmt):
    def __init__(self, ident, expr, no_line, pos):
        self.type = "assstmt"
        self.ident = ident
        self.expr = expr
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.expr.type_check(env, expected_type=env.get_variable_type(self.ident))
        return env

    def return_check(self):
        return False


class IncrStmt(Stmt):
    def __init__(self, ident, no_line, pos):
        self.type = "incrstmt"
        self.ident = ident
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException.SyntaxEception("Increment can be applied only to integers, but got "
                                                 + str(env.get_variable_type(self.ident))
                                                 + " for variable " + self.ident + ".", self.no_line)
        return env

    def return_check(self):
        return False


class DecrStmt(Stmt):
    def __init__(self, ident, no_line, pos):
        self.type = "decrstmt"
        self.ident = ident
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException.SyntaxEception("Decrement can be applied only to integers, but got "
                                                 + str(env.get_variable_type(self.ident))
                                                 + " for variable " + self.ident + ".", self.no_line)
        return env

    def return_check(self):
        return False


class RetStmt(Stmt):
    def __init__(self, expr, no_line):
        self.type = "retstmt"
        self.expr = expr
        self.no_line = no_line

    def type_check(self, env):
        self.expr.type_check(env, expected_type=env.current_fun_type.returntype)
        return env

    def return_check(self):
        return True


class VRetStmt(Stmt):
    def __init__(self, no_line):
        self.type = "vretstmt"
        self.no_line = no_line

    def type_check(self, env):
        if env.current_fun_type.returntype != typeparser.Type("void"):
            raise SyntaxException.SyntaxEception("Incorrect return type, expected not void.", self.no_line)
        return env

    def return_check(self):
        return False


class CondStmt(Stmt):
    def __init__(self, expr, stmt, no_line):
        self.type = "condstmt"
        self.expr = expr
        self.stmt = stmt
        self.no_line = no_line

    def type_check(self, env):
        self.expr.type_check(env, expected_type=typeparser.Type("boolean"))
        self.stmt.type_check(env)
        return env

    def return_check(self):
        if self.expr.value is True:
            return self.stmt.return_check()
        else:
            return False


class CondElseStmt(Stmt):
    def __init__(self, expr, stmt1, stmt2, no_line):
        self.type = "condelsestmt"
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.no_line = no_line

    def type_check(self, env):
        self.expr.type_check(env, expected_type=typeparser.Type("boolean"))
        self.stmt1.type_check(env)
        self.stmt1.type_check(env)
        return env

    def return_check(self):
        if self.expr.value is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.value:
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()


class WhileStmt(Stmt):
    def __init__(self, expr, stmt, no_line):
        self.type = "whilestmt"
        self.expr = expr
        self.stmt = stmt
        self.no_line = no_line

    def type_check(self, env):
        self.expr.type_check(env, expected_type=typeparser.Type("boolean"))
        self.stmt.type_check(env)
        return env

    def return_check(self):
        return self.stmt.return_check()


class SExpStmt(Stmt):
    def __init__(self, expr, no_line):
        self.type = "sexpstmt"
        self.expr = expr
        self.no_line = no_line

    def type_check(self, env):
        self.expr.type_check(env, None)
        return env

    def return_check(self):
        return False