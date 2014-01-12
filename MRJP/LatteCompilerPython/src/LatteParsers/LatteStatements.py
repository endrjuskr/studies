__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["VarAssStmt", "FieldAssStmt", "BStmt", "CondElseStmt", "CondStmt", "DeclStmt", "DecrStmt",
           "EmptyStmt", "IncrStmt", "RetStmt", "SExpStmt", "StmtBase", "VRetStmt", "WhileStmt", "ForStmt",
           "FieldDecrStmt", "FieldIncrStmt", "ArrayAssStmt"]

from .LatteTypes import *
from ..LatteExceptions import *
from .BaseNode import *
from ..Env import *


class StmtBase(BaseNode):
    def __init__(self, type, no_line, pos):
        super(StmtBase, self).__init__(type, no_line, pos)

    def type_check(self, env):
        pass

    def return_check(self):
        return False


class ForStmt(StmtBase):
    def __init__(self, var_ident, type, collection, stmt, no_line, pos):
        super(ForStmt, self).__init__("assstmt", no_line, pos)
        self.var_ident = var_ident
        self.type = Type(type)
        self.collection = collection
        self.stmt = stmt


class VarAssStmt(StmtBase):
    def __init__(self, ident, expr, no_line, pos):
        super(VarAssStmt, self).__init__("varassstmt", no_line, pos)
        self.ident = ident
        self.expr = expr
        self.idtype = None

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.idtype = env.get_variable_type(self.ident)
        self.expr.type_check(env, expected_type=self.idtype)

    def return_check(self):
        return False

    def generate_body(self, env):
        s = self.expr.generate_code_jvm(env)
        if self.idtype == Type("string"):
            s += "astore "
        else:
            s += "istore "

        s += str(env.get_variable_value(self.ident)) + "\n"
        env.pop_stack(1)
        return s

class FieldAssStmt(StmtBase):
    def __init__(self, ident, field, expr, no_line, pos):
        super(FieldAssStmt, self).__init__("fieldassstmt", no_line, pos)
        self.ident = ident
        self.field = field
        self.expr = expr
        self.idtype = None

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.idtype = env.get_variable_type(self.ident)
        self.expr.type_check(env, expected_type=self.idtype)

    def return_check(self):
        return False


class ArrayAssStmt(StmtBase):
    def __init__(self, ident, index, expr, no_line, pos):
        super(ArrayAssStmt, self).__init__("fieldassstmt", no_line, pos)
        self.ident = ident
        self.index = index
        self.expr = expr
        self.idtype = None

    def type_check(self, env):
        if not env.contain_variable(self.ident):
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        self.idtype = env.get_variable_type(self.ident)
        self.expr.type_check(env, expected_type=self.idtype)

    def return_check(self):
        return False


class BStmt(StmtBase):
    def __init__(self, block, no_line):
        super(BStmt, self).__init__("blockstmt", no_line, 0)
        self.block = block

    def type_check(self, env):
        self.block.type_check(env)

    def return_check(self):
        return self.block.return_check()

    def generate_body(self, env):
        env_prim = Env(env)
        s = self.block.generate_code_jvm(env_prim)
        env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
        env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
        return s


class CondElseStmt(StmtBase):
    def __init__(self, expr, stmt1, stmt2, no_line, pos):
        super(CondElseStmt, self).__init__("condelsestmt", no_line, pos)
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.label_pattern = "condelse_" + str(self.no_line) + "_" + str(self.pos)

    def type_check(self, env):
        env_prim = Env(env)
        env_prim2 = Env(env)
        self.expr.type_check(env, expected_type=Type("boolean"))
        self.stmt1.type_check(env_prim)
        self.stmt2.type_check(env_prim2)

    def return_check(self):
        if self.expr.get_value() is None:
            return self.stmt1.return_check() and self.stmt2.return_check()
        elif self.expr.get_value():
            return self.stmt1.return_check()
        else:
            return self.stmt2.return_check()


    def generate_body(self, env):
        if self.expr.get_value() is True:
            env_prim = Env(env)
            s = self.stmt1.generate_code_jvm(env_prim)
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            return s
        elif self.expr.get_value() is False:
            env_prim = Env(env)
            s = self.stmt2.generate_code_jvm(env_prim)
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            return s
        else:
            env_prim = Env(env)
            env_prim2 = Env(env)
            s = self.expr.generate_code_jvm(env)
            s += "ifeq " + self.label_pattern + "_f\n"
            env.pop_stack(1)
            s += self.stmt1.generate_code_jvm(env_prim)
            s += "goto " + self.label_pattern + "\n"
            s += self.label_pattern + "_f:\n"
            s += self.stmt2.generate_code_jvm(env_prim2)
            s += self.label_pattern + ":\n"
            env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
            env.max_variable_counter = max(env.max_variable_counter, env_prim2.get_local_limit())
            env.max_stack_count = max(env.max_stack_count, env_prim2.max_stack_count)
            return s


class CondStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(CondStmt, self).__init__("condstmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt
        self.label_pattern = "cond_" + str(self.no_line) + "_" + str(self.pos)


    def type_check(self, env):
        env_prim = Env(env)
        self.expr.type_check(env, expected_type=Type("boolean"))
        self.stmt.type_check(env_prim)

    def return_check(self):
        if self.expr.get_value() is True:
            return self.stmt.return_check()
        else:
            return False

    def generate_body(self, env):
        env_prim = Env(env)
        s = self.expr.generate_code_jvm(env)
        s += "ifeq " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.stmt.generate_code_jvm(env_prim)
        s += self.label_pattern + ":\n"
        env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
        env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
        return s


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

    def generate_body(self, env):
        s = ""
        for item in self.itemlist:
            s += item.generate_code_jvm(env)
        return s


class DecrStmt(StmtBase):
    def __init__(self, ident, no_line, pos):
        super(DecrStmt, self).__init__("decrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException("Decrement can be applied only to integers, but got "
                                                  + str(env.get_variable_type(self.ident))
                                                  + " for variable " + self.ident + ".", self.no_line)

    def generate_body(self, env):
        return "iinc " + str(env.get_variable_value(self.ident)) + " -1\n"


class FieldDecrStmt(StmtBase):
    def __init__(self, ident, field, no_line, pos):
        super(FieldDecrStmt, self).__init__("decrstmt", no_line, pos)
        self.ident = ident
        self.field = field

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException("Decrement can be applied only to integers, but got "
                                                  + str(env.get_variable_type(self.ident))
                                                  + " for variable " + self.ident + ".", self.no_line)

class EmptyStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(EmptyStmt, self).__init__("emptystmt", no_line, pos)


class IncrStmt(StmtBase):
    def __init__(self, ident, no_line, pos):
        super(IncrStmt, self).__init__("incrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException("Increment can be applied only to integers, but got "
                                                  + str(env.get_variable_type(self.ident))
                                                  + " for variable " + self.ident + ".", self.no_line)

    def generate_body(self, env):
        return "iinc " + str(env.get_variable_value(self.ident)) + " 1\n"


class FieldIncrStmt(StmtBase):
    def __init__(self, ident, field, no_line, pos):
        super(FieldIncrStmt, self).__init__("incrstmt", no_line, pos)
        self.ident = ident
        self.field = field

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException("Increment can be applied only to integers, but got "
                                                  + str(env.get_variable_type(self.ident))
                                                  + " for variable " + self.ident + ".", self.no_line)


class RetStmt(StmtBase):
    def __init__(self, expr, no_line, pos):
        super(RetStmt, self).__init__("retstmt", no_line, pos)
        self.expr = expr

    def type_check(self, env):
        self.expr.type_check(env, expected_type=env.current_fun_type.return_type)

    def return_check(self):
        return True

    def generate_body(self, env):
        s = self.expr.generate_code_jvm(env)
        if env.in_main:
            s += "invokestatic java/lang/System/exit(I)V\n"
            s += "return\n"
        elif env.current_fun_type.return_type == Type("string"):
            s += "areturn \n"
        else:
            s += "ireturn \n"
        env.pop_stack(1)
        return s


class SExpStmt(StmtBase):
    def __init__(self, expr, no_line, pos):
        super(SExpStmt, self).__init__("sexpstmt", no_line, pos)
        self.expr = expr

    def type_check(self, env):
        # Here we assume that the only expression is invocation of void function.
        self.expr.type_check(env, expected_type=Type("void"))

    def generate_body(self, env):
        return self.expr.generate_code_jvm(env)


class VRetStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(VRetStmt, self).__init__("vretstmt", no_line, pos)

    def type_check(self, env):
        if env.current_fun_type.return_type != Type("void"):
            raise SyntaxException("Incorrect return type, expected not void.", self.no_line,
                                                  pos=self.pos)

    def generate_body(self, env):
        return "return \n"


class WhileStmt(StmtBase):
    def __init__(self, expr, stmt, no_line, pos):
        super(WhileStmt, self).__init__("whilestmt", no_line, pos)
        self.expr = expr
        self.stmt = stmt
        self.label_pattern = "while_" + str(self.no_line) + "_" + str(self.pos)

    def type_check(self, env):
        env_prim = Env(env)
        self.expr.type_check(env, expected_type=Type("boolean"))
        self.stmt.type_check(env_prim)

    def return_check(self):
        return self.stmt.return_check()

    def generate_body(self, env):
        env_prim =Env(env)
        s = self.label_pattern + "_w:\n"
        s += self.expr.generate_code_jvm(env)
        s += "ifeq " + self.label_pattern + "\n"
        env.pop_stack(1)
        s += self.stmt.generate_code_jvm(env_prim)
        s += "goto " + self.label_pattern + "_w\n"
        s += self.label_pattern + ":\n"
        env.max_variable_counter = max(env.max_variable_counter, env_prim.get_local_limit())
        env.max_stack_count = max(env.max_stack_count, env_prim.max_stack_count)
        return s
