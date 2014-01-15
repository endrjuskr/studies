__author__ = 'Andrzej Skrodzki - as292510'

import sys
import subprocess

import lattepar
import lattelex
from .LatteExceptions import *
from LatteParsers import *
from .Env import *


def print_usage():
    print "##############"
    print "\n  latc - latte compiler written in python using PLY.\n"
    print "\tUsage:\n"
    print "  latc [file] - passing file to compile.\n"
    print "  latc help - showing usage.\n"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Please provide file name.\n"
        print_usage()
        sys.exit(-1)
    if sys.argv[1] == "help":
        print_usage()
        sys.exit()

    path = sys.argv[1].split('/')
    program_file = path[len(path) - 1]
    program_name = program_file.split('.')[0]

    try:
        with open(sys.argv[1], 'r') as content_file:
            content = content_file.read()

    except IOError:
        print "File does not exist - '{}'.".format(sys.argv[1])
        sys.exit(-1)
    asm = 0
    if len(sys.argv) > 2:
        asm = 1

    lattelexer = lattelex.get_lexer()
    latteparser = lattepar.get_parser()
    result = latteparser.parse(content, lexer=lattelexer)
    if len(lattepar.exception_list) != 0:
        sys.stderr.write("ERROR\n")
        for ex in lattepar.exception_list:
            ex.find_column(content)
            sys.stderr.write("{}\n".format(ex))
        sys.exit(-2)
    if result is None:
        sys.stderr.write("ERROR\n")
        sys.stderr.write("Unexpected end of file.\n")
    result.set_class_name(program_name)
    result.type_check()

    ex_li = exception_list_env
    ex_li += LatteExpressions.exception_list_expr
    ex_li += LatteStatements.exception_list_stmt
    ex_li += LatteTopDefinitions.exception_list_fn

    if len(ex_li) != 0:
        sys.stderr.write("ERROR\n")
        for ex in ex_li:
            ex.find_column(content)
            sys.stderr.write("{}\n".format(ex))
        sys.exit(-2)

    # At this point lexer and syntax analysis is done so program is accepted.
    sys.stderr.write("OK\n")
    path[len(path) - 1] = program_name + (".j" if asm == 0 else ".s")
    new_file_path = '/'.join(path)
    path[len(path) - 1] = program_name + ".o"
    obj_file_path = '/'.join(path)
    if asm == 0:
        f = open(new_file_path, 'w+')
        f.write(result.generate_code_jvm(Env(class_name=program_name)))
        f.close()
        subprocess.call("java -cp lib/*.class -jar lib/jasmin.jar -g -d " + '/'.join(path[0:-1])
                        + " " + new_file_path, shell=True)
    else:
        f = open(new_file_path, 'w+')
        f.write(result.generate_code_asm(Env(class_name=program_name)))
        f.close()
        subprocess.call("nasm -g -f elf64 " + new_file_path, shell=True)
        subprocess.call("gcc -g lib/runtime.o " + obj_file_path, shell=True)
    sys.exit()
