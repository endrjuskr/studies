__author__ = 'andrzejskrodzki'
import sys
import lattepar
import lattelex
import lattetypechecker
from LatteExceptions import SyntaxException

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print "Please provide file name."
        sys.exit(-1)
    with open(sys.argv[1], 'r') as content_file:
        content = content_file.read()
        # Build the parser
    debug = 0
    print_tokens = 0
    lattelexer = lattelex.get_lexer()
    latteparser = lattepar.get_parser()
    if len(sys.argv) > 2:
        debug = 1
    if len(sys.argv) > 3:
        lattelexer.input(content)
        while True:
            tok = lattelexer.token()
            if not tok: break      # No more input
            print tok.type, tok.value, tok.lexpos
    try:
        result = latteparser.parse(content, lexer=lattelexer, debug=debug, tracking=True)
        if result is None:
            raise SyntaxException.SyntaxException("Something happened wrong, but compiler could not find out :(.", 0)
        lattechecker = lattetypechecker.TypeCheck(result)
        lattechecker.full_check()
    except BaseException as e:
        sys.stderr.write("ERROR\n")
        sys.stderr.write("{}\n".format(e))
        sys.stdout.write("{}\n".format(e))
        sys.exit(-2)

    sys.stderr.write("OK\n")
    sys.exit()
