__author__ = 'Andrzej Skrodzki - as292510'
import sys
import lattepar
import lattelex
from LatteExceptions import *


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
    try:
        with open(sys.argv[1], 'r') as content_file:
            content = content_file.read()

    except IOError:
        print "File does not exist - '{}'.".format(sys.argv[1])
        sys.exit(-1)
    debug = 0
    if len(sys.argv) > 2:
        debug = 1 if sys.argv[2] == "-d" else 0

    lattelexer = lattelex.get_lexer()
    latteparser = lattepar.get_parser()
    try:
        result = latteparser.parse(content, lexer=lattelexer)
        if result is None:
            raise SyntaxException.SyntaxException("Something happened wrong, but compiler could not find out :(.", -1)
        result.type_check()
        f = open('myprog.j', 'r+')
        f.write(result.generate_code())
    except BaseException.BaseException as e:
        sys.stderr.write("ERROR\n")
        e.find_column(content)
        sys.stderr.write("{}\n".format(e))
        sys.stdout.write("{}\n".format(e))
        sys.exit(-2)

    sys.stderr.write("OK\n")
    sys.exit()
