__author__ = 'andrzejskrodzki'

import typeparser


class Stmt:
    pass


class Block:
    def __init__(self, stmtlist):
        self.type = "block"
        self.stmtlist = stmtlist

    def type_check(self, env):
        env_prim = env.copy()
        for stmt in self.stmtlist:
            print stmt
            env_prim = stmt.type_check(env_prim)
        return env

    def return_check(self):
        for i in range(len(self.stmtlist)):
            if self.stmtlist[i]:
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
            print item.itemtype
            env.add_variable(item.ident, item.itemtype, self.no_line, fun_param=False)
        return env

    def return_check(self):
        return False


class Item:
    pass


class NoInitItem(Item):
    def __init__(self, ident):
        self.type = "noinititem"
        self.ident = ident
        self.itemtype = "unknown"

    def type_check(self, env):
        pass


class InitItem(Item):
    def __init__(self, ident, expr):
        self.type = "inititem"
        self.ident = ident
        self.expr = expr
        self.itemtype = "unknown"

    def type_check(self, env):
        self.expr.type_check(env, expected_type=self.itemtype)


class AssStmt(Stmt):
    def __init__(self, ident, expr, no_line):
        self.type = "assstmt"
        self.ident = ident
        self.expr = expr
        self.no_line = no_line

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            print "Variable not declared."
            exit(-1)
        print "test", env.get_variable_type(self.ident)
        self.expr.type_check(env, expected_type=env.get_variable_type(self.ident))
        return env

    def return_check(self):
        return False


class IncrStmt(Stmt):
    def __init__(self, ident, no_line):
        self.type = "incrstmt"
        self.ident = ident
        self.no_line = no_line

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            print "Variable is not declared in the scope"
            exit(-1)
        elif env.get_variable_type(self.ident).type != "int":
            print "Increment can be applied only to integers."
            exit(-1)
        return env


    def return_check(self):
        return False


class DecrStmt(Stmt):
    def __init__(self, ident, no_line):
        self.type = "decrstmt"
        self.ident = ident
        self.no_line = no_line

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            print "Variable is not declared in the scope"
            exit(-1)
        elif env.get_variable_type(self.ident).type != "int":
            print "Decrement can be applied only to integers."
            exit(-1)
        return env

    def return_check(self):
        return False


class RetStmt(Stmt):
    def __init__(self, expr, no_line):
        self.type = "retstmt"
        self.expr = expr
        self.no_line = no_line

    def type_check(self, env):
        print self.no_line
        if env.current_fun_type.returntype == typeparser.Type("void"):
            print "Incorrrect return type. Expected void."
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
            print "Incorrect return type. Expected not void."
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
        return self.stmt1.return_check() and self.stmt2.return_check()


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
        self.expr.type_check(env)
        return env

    def return_check(self):
        return False