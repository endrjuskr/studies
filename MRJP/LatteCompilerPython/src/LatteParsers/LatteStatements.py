__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["VarAssStmt", "BStmt", "CondElseStmt", "CondStmt", "DeclStmt", "DecrStmt",
           "EmptyStmt", "IncrStmt", "RetStmt", "SExpStmt", "StmtBase", "VRetStmt", "WhileStmt", "ForStmt",
            "exception_list_stmt"]

from .LatteTypes import *
from ..LatteExceptions import *
from .BaseNode import *
from ..Env import *

exception_list_stmt = []


class StmtBase(BaseNode):
    def __init__(self, type, no_line, pos):
        super(StmtBase, self).__init__(type, no_line, pos)

    def type_check(self, env):
        pass

    def return_check(self):
        return False


class VarAssStmt(StmtBase):
    def __init__(self, ident, expr, no_line, pos):
        super(VarAssStmt, self).__init__("varassstmt", no_line, pos)
        self.ident = ident
        self.expr = expr
        self.idtype = None

    def type_check(self, env):
        self.ident.type_check(env)
        self.idtype = env.get_variable_type(self.ident.get_id())
        self.expr.type_check(env, expected_type=self.idtype)

    def return_check(self):
        return False

    def generate_body(self, env):
        s = self.expr.generate_code_jvm(env)
        if self.idtype == Type("string"):
            s += "astore "
        else:
            s += "istore "

        s += str(env.get_variable_value(self.ident.get_id())) + "\n"
        env.pop_stack(1)
        return s

    def generate_code_asm(self, env, get_value=True):
        s = self.expr.generate_code_asm(env, get_value)
        env.increment_stack()
        if self.idtype.is_array():
            env.increment_stack()

        s += self.ident.generate_code_asm(env, get_value=False)
        env.decrement_stack()
        if self.idtype.is_array():
            env.decrement_stack()

        s += "pop rbx\n"
        s += "pop rax\n"
        if self.idtype.is_array():
            s += "pop rcx\n"
        s += "mov [rbx], rax\n"
        if self.idtype.is_array():
            s += "mov [rbx + 8], rcx\n"

        return s


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

    def generate_code_asm(self, env, get_value=True):
        env_prim = Env(env)
        s = self.block.generate_code_asm(env_prim)
        s += "add rsp, " + str((env_prim.variables_counter - env.variables_counter) * 8) + "\n"
        env.string_dict = env_prim.string_dict
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

    def generate_code_asm(self, env, get_value=True):
        if self.expr.get_value() is True:
            env_prim = Env(env)
            s = self.stmt1.generate_code_asm(env_prim)
            env.string_dict = env_prim.string_dict
            return s
        elif self.expr.get_value() is False:
            env_prim = Env(env)
            s = self.stmt2.generate_code_asm(env_prim)
            env.string_dict = env_prim.string_dict
            return s
        else:
            env_prim = Env(env)
            env_prim2 = Env(env)
            s = self.expr.generate_code_asm(env, get_value)
            s += "pop rax\n"
            s += "cmp rax, 0\n"
            s += "je " + self.label_pattern + "_f\n"
            s += self.stmt1.generate_code_asm(env_prim)
            env_prim2.string_dict = env_prim.string_dict
            s += "jmp " + self.label_pattern + "\n"
            s += self.label_pattern + "_f:\n"
            s += self.stmt2.generate_code_asm(env_prim2)
            s += self.label_pattern + ":\n"
            env.string_dict = env_prim2.string_dict
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

    def generate_code_asm(self, env, get_value=True):
        env_prim = Env(env)
        s = self.expr.generate_code_asm(env, get_value)
        s += "pop rax\n"
        s += "cmp rax, 0\n"
        s += "je " + self.label_pattern + "\n"
        s += self.stmt.generate_code_asm(env_prim)
        s += self.label_pattern + ":\n"
        env.string_dict = env_prim.string_dict
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

    def generate_code_asm(self, env, get_value=True):
        s = ""
        for item in self.itemlist:
            s += item.generate_code_asm(env, get_value)
        return s


class DecrStmt(StmtBase):
    def __init__(self, ident, no_line, pos):
        super(DecrStmt, self).__init__("decrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        t = env.get_variable_type(self.ident.get_id())
        if t is not None and t.type != "int":
            exception_list_stmt.append(SyntaxException("Decrement can be applied only to integers.", self.no_line))

    def generate_body(self, env):
        return "iinc " + str(env.get_variable_value(self.ident.get_id())) + " -1\n"

    def generate_code_asm(self, env, get_value=True):
        s = self.ident.generate_code_asm(env, get_value=False)
        s += "pop rax\n"
        s += "dec qword [rax]\n"
        return s


class EmptyStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(EmptyStmt, self).__init__("emptystmt", no_line, pos)


class IncrStmt(StmtBase):
    def __init__(self, ident, no_line, pos):
        super(IncrStmt, self).__init__("incrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        t = env.get_variable_type(self.ident.get_id())
        if t is not None and t.type != "int":
            exception_list_stmt.append(SyntaxException("Increment can be applied only to integers.", self.no_line))

    def generate_body(self, env):
        return "iinc " + str(env.get_variable_value(self.ident.get_id())) + " 1\n"

    def generate_code_asm(self, env, get_value=True):
        s = self.ident.generate_code_asm(env, get_value=False)
        s += "incr_" + str(self.no_line) + ":\npop rax\n"
        s += "inc qword [rax]\n"
        return s


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

    def generate_code_asm(self, env, get_value=True):
        s = self.expr.generate_code_asm(env, get_value)
        s += "pop rax\n"
        if self.expr.etype.is_array():
            s += "pop rbx\n"
        s += "leave\nret\n"
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

    def generate_code_asm(self, env, get_value=True):
        return self.expr.generate_code_asm(env, get_value)


class VRetStmt(StmtBase):
    def __init__(self, no_line, pos):
        super(VRetStmt, self).__init__("vretstmt", no_line, pos)

    def type_check(self, env):
        if env.current_fun_type.return_type != Type("void"):
            exception_list_stmt.append(SyntaxException("Incorrect return type, expected not void.", self.no_line,
                                                  pos=self.pos))

    def generate_body(self, env):
        return "return \n"

    def generate_code_asm(self, env, get_value=True):
        return "mov rax, 0\nleave\nret\n"


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
        env_prim = Env(env)
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

    def generate_code_asm(self, env, get_value=True):
        env_prim = Env(env)
        s = self.label_pattern + "_w:\n"
        s += self.expr.generate_code_asm(env, get_value)
        s += "pop rax\n"
        s += "cmp rax, 0\n"
        s += "je " + self.label_pattern + "\n"
        s += self.stmt.generate_code_asm(env_prim)
        s += "jmp " + self.label_pattern + "_w\n"
        s += self.label_pattern + ":\n"
        env.string_dict = env_prim.string_dict
        return s


class ForStmt(StmtBase):
    def __init__(self, var_ident, type, collection, stmt, no_line, pos):
        super(ForStmt, self).__init__("assstmt", no_line, pos)
        self.var_ident = var_ident
        self.type = type
        self.collection = collection
        self.stmt = stmt
        self.label = "for_" + str(self.no_line) + "_" + str(self.pos)

    def type_check(self, env):
        if self.type.get_type() == Type("void"):
            exception_list_stmt.append(SyntaxException("Type void is not allowed.", self.no_line, self.pos))
        if self.type.is_array():
            exception_list_stmt.append(SyntaxException("Multidimensional arrays are not allowed.", self.no_line, self.pos))

        env_prim = Env(env)
        env_prim.add_variable(self.var_ident, self.type, self.no_line, self.pos, False)
        self.collection.type_check(env, expected_type=ArrayType(self.type))
        self.stmt.type_check(env_prim)

    def return_check(self):
        return self.stmt.return_check()

    def generate_code_asm(self, env, get_value=True):
        s = self.collection.generate_code_asm(env, get_value=True)
        s += "push 0\n"
        s += self.label + "_f:\n"
        s += "mov rcx, [rsp]\n"
        s += "cmp rcx, [rsp + 16]\n"
        s += "jge " + self.label + "\n"
        env_prim = Env(env)
        env_prim.variables_counter += 3
        env_prim.add_variable(self.var_ident, self.type, self.no_line, self.pos, False)
        s += "mov rax, [rsp+8]\n"
        s += "shl rcx, 3\n"
        s += "add rax, rcx\n"
        s += "push qword [rax]\n"
        s += self.stmt.generate_code_asm(env_prim)
        s += "pop rax\n"
        s += "inc qword [rsp]\n" # next index
        s += "jmp " + self.label + "_f\n"
        env.string_dict = env_prim.string_dict
        s += self.label + ":\n"
        s += "pop rax\n"
        s += "pop rax\n"
        s += "pop rax\n"
        return s
