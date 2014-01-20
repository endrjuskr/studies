__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["Block", "FnDef", "Program", "PredefinedFun", "ClassDef", "exception_list_fn"]

from ..LatteExceptions import *
from .LatteTypes import *
from .BaseNode import *
from ..Env import *

exception_list_fn = []

class Block(BaseNode):
    def __init__(self, stmt_list):
        super(Block, self).__init__("block", 0, 0)
        self.stmt_list = stmt_list

    def type_check(self, env, reset_declarations=True):
        env_prim = Env(env, reset_declarations=reset_declarations)
        for stmt in self.stmt_list:
            stmt.type_check(env_prim)

    def return_check(self):
        for stmt in self.stmt_list:
            if stmt.return_check():
                return True
        return False

    def generate_body(self, env):
        s = ""
        for stmt in self.stmt_list:
            s += stmt.generate_code_jvm(env)
        return s

    def generate_code_asm(self, env, get_value=True):
        s = ""
        for stmt in self.stmt_list:
            s += stmt.generate_code_asm(env, get_value)
        return s


class ClassDef(BaseNode):
    def __init__(self, ident, extlist, fieldlist, no_line):
        super(ClassDef, self).__init__("classdef", no_line, 0)
        self.ident = ident
        methods =  filter(lambda x: hasattr(x, "block"), fieldlist)
        fields = filter(lambda x: not hasattr(x, "block"), fieldlist)
        self.fieldpositions = map(lambda x: x.ident, fields)
        self.fieldlist = dict(zip(map(lambda x: x.ident, fields), fields))
        self.methodslist = dict(zip(map(lambda x: x.ident, methods), methods))
        self.methodslist_2 = dict(zip(map(lambda x: x.ident, methods), methods))
        self.extlist = extlist
        self.derived = False
        self.size_s = 0
        self.vis = False

    def prepare_env(self, env):
        env.add_variable("self", Type(self.ident), 0, 0)
        for f in self.fieldpositions:
            v = self.fieldlist[f]
            if v.field_type.is_array():
                env.add_variable(v.ident, None, 0, 0)
            env.add_variable(v.ident, v.field_type, v.no_line, v.pos, is_field=True)

    def get_size(self):
        return self.size_s

    def get_derived(self, env):
        if self.vis:
            exception_list_fn.append(SyntaxException("Cycle in inheritance.", 0))
            return None
        if self.derived:
            return
        self.vis = True
        self.derived = True
        if len(self.extlist) != 0:
            cl = env.get_class(self.extlist[0])
            if cl is not None:
                cl.get_derived(env)
                self.fieldpositions = cl.fieldpositions + self.fieldpositions
                for k, v in cl.fieldlist.iteritems():
                    self.fieldlist[k] = v
                for k, v in cl.methodslist.iteritems():
                    if k in self.methodslist:
                        exception_list_fn.append(SyntaxException("Overriding method is not possible - " + k, 0))
                    self.methodslist[k] = v
        for f in self.fieldpositions:
            v = self.fieldlist[f]
            if v.field_type.is_array():
                self.size_s += 1
            self.size_s += 1
        self.vis = False

    def get_field_position(self, ident):
        index = 0
        for f in self.fieldpositions:
            v = self.fieldlist[f]
            if v.ident == ident:
                return index
            if v.field_type.is_array():
                index += 1
            index += 1


    def type_check(self, env):
        env_p = Env(env)
        for fn in self.methodslist.values():
            env_p.add_fun(fn)
        for fn in self.methodslist.values():
            env_prim = Env(env_p)
            self.prepare_env(env_prim)
            fn.type_check(env_prim)

    def contain_field(self, field):
        return field in self.fieldlist

    def contain_method(self, method):
        return method in self.methodslist

    def get_field_type(self, field):
        if not field in self.fieldlist:
            return None
        return self.fieldlist[field].field_type

    def get_method_type(self, method):
        if not method in self.methodslist:
            return None
        return self.methodslist[method].funtype

    def generate_code_asm(self, env, get_value=True):
        s = ""
        s_dict = env.string_dict
        for fn in self.methodslist_2.values():
            env_prim = Env(env)
            self.prepare_env(env_prim)
            env_prim.string_dict = s_dict
            fn.is_class_method = True
            fn.class_id = self.ident
            s += fn.generate_code_asm(env_prim)
            s_dict = env_prim.string_dict

        env.string_dict = s_dict

        return s


class FnDef(BaseNode):
    def __init__(self, type, ident, arglist, block, no_line):
        super(FnDef, self).__init__("fndef", no_line, 0)
        self.funtype = self.calculate_type(type, arglist)
        self.ident = ident
        self.arglist = arglist
        self.block = block
        self.is_class_method = False
        self.class_id = None

    def get_type(self, arg):
        return arg.argtype

    def type_check(self, env):
        self.prepare_env(env)
        for arg in self.arglist:
            arg.type_check(env)
        self.block.type_check(env, reset_declarations=False)
        if not self.funtype.return_type == Type("void"):
            if not self.block.return_check():
                exception_list_fn.append(ReturnException(self.ident, self.no_line))

    def prepare_env(self, env):
        #if self.is_class_method:
        #    env.add_variable("self", Type(self.class_id), 0, 0)
        for arg in self.arglist:
            if arg.argtype.is_array():
                env.add_variable(arg.ident, None, 0, 0)
            env.add_variable(arg.ident, arg.argtype, arg.no_line, arg.pos)
        env.current_fun_type = self.funtype
        env.in_main = self.ident == "main"
        if self.is_class_method:
            env.class_name = self.class_id

    def calculate_type(self, type, arglist):
        return FunType(type, map(self.get_type, arglist))

    def generate_header(self):
        return ".method public static " + self.ident + self.funtype.generate_code_jvm() + "\n" if  \
            self.ident != "main" else ".method public static main([Ljava/lang/String;)V \n"

    def generate_body(self, env):
        self.prepare_env(env)
        if self.ident == "main":
            env.add_variable("args", Type("string"), 0, 0)
        s = self.block.generate_code_jvm(env)
        s += "return\n"
        s = ".limit stack " + str(env.get_stack_limit()) + "\n.limit locals " + str(env.get_local_limit()) + "\n" + s
        return s

    def generate_footer(self):
        return ".end method \n"

    def generate_code_asm(self, env, get_value=True):
        s = "o_" if self.is_class_method else ""
        s += self.ident + ":\n"
        self.prepare_env(env)
        s += "enter 0, 0\n"
        env.variables_counter += 1
        if not self.ident == "main":
            env.variables_counter += 1
        s += self.block.generate_code_asm(env, get_value)
        if not s.endswith("ret\n"):
            s += "leave\n"
            s += "ret\n"
        return s


class PredefinedFun(FnDef):
    def __init__(self, type, ident, arglist):
        super(PredefinedFun, self).__init__(type, ident, arglist, [], 0)

    def type_check(self, env):
        pass

    def calculate_type(self, type, arglist):
        return FunType(type, arglist)

    def generate_code_jvm(self, env):
        return ""

    def generate_code_asm(self, env, get_value=True):
        return ""


class ErrorFun(PredefinedFun):
    def __init__(self):
        super(ErrorFun, self).__init__(Type("void"), "error", [])


class PrintIntFun(PredefinedFun):
    def __init__(self):
        super(PrintIntFun, self).__init__(Type("void"), "printInt", [Type("int")])


class PrintStringFun(PredefinedFun):
    def __init__(self):
        super(PrintStringFun, self).__init__(Type("void"), "printString", [Type("string")])


class ReadIntFun(PredefinedFun):
    def __init__(self):
        super(ReadIntFun, self).__init__(Type("int"), "readInt", [])


class ReadStringFun(PredefinedFun):
    def __init__(self):
        super(ReadStringFun, self).__init__(Type("string"), "readString", [])


class ConcatenateStringFun(PredefinedFun):
    def __init__(self):
        super(ConcatenateStringFun, self).__init__(Type("string"), "concatenateString",
                                                   [Type("string"), Type("string")])

class Program(BaseNode):
    def __init__(self, topdeflist):
        super(Program, self).__init__("program", -1, 0)
        self.topdeflist = topdeflist
        self.topdeflist.append(ErrorFun())
        self.topdeflist.append(ReadIntFun())
        self.topdeflist.append(ReadStringFun())
        self.topdeflist.append(PrintStringFun())
        self.topdeflist.append(PrintIntFun())
        self.topdeflist.append(ConcatenateStringFun())
        self.class_name = "MyClass"

    def type_check(self):
        env = Env()
        for fndef in filter(lambda x: not hasattr(x, "methodslist"), self.topdeflist):
            env.add_fun(fndef)

        for classdef in filter(lambda x: hasattr(x, "methodslist"), self.topdeflist):
            env.add_class(classdef)

        for classdef in filter(lambda x: hasattr(x, "methodslist"), self.topdeflist):
            classdef.get_derived(env)

        if len(exception_list_fn) > 0:
            return

        for fndef in filter(lambda x: not hasattr(x, "methodslist"), self.topdeflist):
            self.fun_check(fndef, env)

        for classdef in filter(lambda x: hasattr(x, "methodslist"), self.topdeflist):
            env_prim = Env(env)
            classdef.type_check(env_prim)

        if env.contain_main() is False:
            exception_list_fn.append(SyntaxException("Main funtion is not declared.", self.no_line))

    def fun_check(self, fun, env):
        env_prim = Env(env)
        fun.type_check(env_prim)

    def generate_body(self, env):
        for fndef in self.topdeflist:
            env.add_fun(fndef)

        s = ""
        for fn in self.topdeflist:
            env_prim = Env(env)
            s += fn.generate_code_jvm(env_prim)
        return s

    def set_class_name(self, name):
        self.class_name = name

    def generate_header(self):
        return ".class public " + self.class_name + \
                "\n.super java/lang/Object \n \
                .method public <init>()V \n \
                aload_0 \n \
                invokespecial java/lang/Object/<init>()V \n \
                return \n \
                .end method \n"

    def generate_code_asm(self, env, get_value=True):
        s = "; Code generated by LatteCompiler\n"
        s += "section .text\n"
        s += "global main\n"
        s += "extern printInt, printString, readInt, readString, error, contactString, calloc, malloc\n"

        for fndef in filter(lambda x: not hasattr(x, "methodslist"), self.topdeflist):
            env.add_fun(fndef)

        for classdef in filter(lambda x: hasattr(x, "methodslist"), self.topdeflist):
            env.add_class(classdef)

        s_dict = {"string_empty": "\"\""}
        for fn in self.topdeflist:
            env_prim = Env(env)
            env_prim.string_dict = s_dict
            s += fn.generate_code_asm(env_prim)
            s_dict = env_prim.string_dict

        h = ""
        if len(s_dict) > 0:
            h += "section .data\n"
            for k, v in s_dict.iteritems():
                h += k + " db " + v + ",0\n"
        return s + h