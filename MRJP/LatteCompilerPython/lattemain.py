__author__ = 'andrzejskrodzki'
import sys
import lattepar
import lattelex

if __name__ == "__main__":
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
    result = latteparser.parse(content, lexer = lattelexer, debug = debug)
    if result is None:
        print "ERR"
    else:
        print "OK"