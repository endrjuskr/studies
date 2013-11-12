__author__ = 'andrzejskrodzki'


class Stmt:
    pass


class Block:
    def __init__(self, stmtlist):
        self.type = "block"
        self.stmtlist = stmtlist

    def type_check(self, env):
        old_env = env.copy()
        for stmt in self.stmtlist:
            env = stmt.type_check(env)
        return old_env

    def return_check(self):
        for i in [1..len(self.stmtlist)]:
            if self.stmtlist[i -1]:
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
    def __init__(self, itemtype, itemlist):
        self.type = "declstmt"
        self.itemtype = itemtype
        self.itemlist = itemlist
        self.settypes()

    def settypes(self):
        for item in self.itemlist:
            item.itemtype = self.itemtype

    def type_check(self, env):
        for item in self.itemlist:
            item.type_check(env)
            env.add_variable(item.ident, item.get_type(), fun_param=False)
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
        self.expr.type_check(env, expected_type = self.itemtype)


class AssStmt(Stmt):
    def __init__(self, ident, expr):
        self.type = "assstmt"
        self.ident = ident
        self.expr = expr

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            print "Variable not declared."
            exit(-1)
        self.expr.type_check(env, expected_type = env.get_variable_type(self.ident))
        return env

    def return_check(self):
        return False


class IncrStmt(Stmt):
    def __init__(self, ident):
        self.type = "incrstmt"
        self.ident = ident

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
    def __init__(self, ident):
        self.type = "decrstmt"
        self.ident = ident

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
    def __init__(self, expr):
        self.type = "retstmt"
        self.expr = expr

    def type_check(self, env):
        if env.current_fun_type.returntype == "void":
            print "Incorrrect return type. Expected void."
        self.expr.type_check(env, expected_type = env.current_fun_type.returntype)
        return env

    def return_check(self):
        return True


class VRetStmt(Stmt):
    def __init__(self):
        self.type = "vretstmt"
    def type_check(self, env):
        if env.current_fun_type.returntype != "void":
            print "Incorrect return type. Expected not void."
        self.expr.type_check(env, env.current_fun_type.returntype)
        return env

    def return_check(self):
        return False

class CondStmt(Stmt):
    def __init__(self, expr, stmt):
        self.type = "condstmt"
        self.expr = expr
        self.stmt = stmt

    def type_check(self, env):
        self.expr.type_check(env, expected_type = "boolean")
        self.stmt.type_check(env)

    def return_check(self):
        return False


class CondElseStmt(Stmt):
    def __init__(self, expr, stmt1, stmt2):
        self.type = "condelsestmt"
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def type_check(self, env):
        self.expr.type_check(env, expected_type = "boolean")
        self.stmt1.type_check(env)
        self.stmt1.type_check(env)

    def return_check(self):
        return self.stmt1.return_check() and self.stmt2.return_check()

class WhileStmt(Stmt):
    def __init__(self, expr, stmt):
        self.type = "whilestmt"
        self.expr = expr
        self.stmt = stmt

    def type_check(self, env):
        self.expr.type_check(env, expected_type = "boolean")
        self.stmt.type_check(env)

    def return_check(self):
        return self.stmt.return_check()

class SExpStmt(Stmt):
    def __init__(self, expr):
        self.type = "sexpstmt"
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env)

    def return_check(self):
        return False