__author__ = 'andrzejskrodzki'

import typeparser
from LatteExceptions import NotDeclaredException, SyntaxException


class Stmt(object):
    def __init__(self, type, no_line, pos):
        self.type = type
        self.no_line = no_line
        self.pos = pos

    def type_check(self, env):
        return env

    def return_check(self):
        return False


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
    def __init__(self, no_line, pos):
        super(EmptyStmt, self).__init__("emptystmt", no_line, pos)

class BStmt(Stmt):
    def __init__(self, block, no_line):
        super(BStmt, self).__init__("blockstmt", no_line, 0)
        self.block = block

    def type_check(self, env):
        return self.block.type_check(env)

    def return_check(self):
        return self.block.return_check()


class DeclStmt(Stmt):
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


class Item(object):
    def __init__(self, ident, no_line, pos, type):
        self.ident = ident
        self.itemtype = "unknown"
        self.no_line = no_line
        self.pos = pos
        self.type = type

    def type_check(self, env):
        pass


class NoInitItem(Item):
    def __init__(self, ident, no_line, pos):
        super(NoInitItem, self).__init__(ident, no_line, pos, "noinititem")


class InitItem(Item):
    def __init__(self, ident, expr, no_line, pos):
        super(InitItem, self).__init__(ident, no_line, pos, "inititem")
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env, expected_type=self.itemtype)


class AssStmt(Stmt):
    def __init__(self, ident, expr, no_line, pos):
        super(AssStmt, self).__init__("assstmt", no_line, pos)
        self.ident = ident
        self.expr = expr

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.expr.type_check(env, expected_type=env.get_variable_type(self.ident))
        return env

    def return_check(self):
        return False


class IncrStmt(Stmt):
    def __init__(self, ident, no_line, pos):
        super(IncrStmt, self).__init__("incrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException.SyntaxException("Increment can be applied only to integers, but got "
                                                 + str(env.get_variable_type(self.ident))
                                                 + " for variable " + self.ident + ".", self.no_line)
        return env


class DecrStmt(Stmt):
    def __init__(self, ident, no_line, pos):
        super(DecrStmt, self).__init__("decrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException.SyntaxException("Decrement can be applied only to integers, but got "
                                                 + str(env.get_variable_type(self.ident))
                                                 + " for variable " + self.ident + ".", self.no_line)
        return env


class RetStmt(Stmt):
    def __init__(self, expr, no_line, pos):
        super(RetStmt, self).__init__("retstmt", no_line, pos)
        self.expr = expr


    def type_check(self, env):
        self.expr.type_check(env, expected_type=env.current_fun_type.returntype)
        return env

    def return_check(self):
        return True


class VRetStmt(Stmt):
    def __init__(self, no_line, pos):
        super(VRetStmt, self).__init__("vretstmt", no_line, pos)

    def type_check(self, env):
        if env.current_fun_type.returntype != typeparser.Type("void"):
            raise SyntaxException.SyntaxException("Incorrect return type, expected not void.", self.no_line)
        return env

class CondStmt(Stmt):
    def __init__(self, expr, stmt, no_line, pos):
        super(CondStmt, self).__init__("condstmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt


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
    def __init__(self, expr, stmt1, stmt2, no_line, pos):
        super(CondElseStmt, self).__init__("condelsestmt", no_line, pos)
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def type_check(self, env):
        self.expr.type_check(env, expected_type=typeparser.Type("boolean"))
        self.stmt1.type_check(env)
        self.stmt2.type_check(env)
        return env

    def return_check(self):
        if self.expr.value is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.value:
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()


class WhileStmt(Stmt):
    def __init__(self, expr, stmt, no_line, pos):
        super(WhileStmt, self).__init__("whilestmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt

    def type_check(self, env):
        self.expr.type_check(env, expected_type=typeparser.Type("boolean"))
        self.stmt.type_check(env)
        return env

    def return_check(self):
        return self.stmt.return_check()


class SExpStmt(Stmt):
    def __init__(self, expr, no_line, pos):
        super(SExpStmt, self).__init__("sexpstmt", no_line, pos)
        self.expr = expr

    def type_check(self, env):
        # Here we assume that the only expression is invocation of void function.
        self.expr.type_check(env, expected_type=typeparser.Type("void"))
        return env