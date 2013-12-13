from StmtBase import StmtBase
from LatteExceptions import SyntaxException


class IncrStmt(StmtBase):
    def __init__(self, ident, no_line, pos):
        super(IncrStmt, self).__init__("incrstmt", no_line, pos)
        self.ident = ident

    def type_check(self, env):
        if env.get_variable_type(self.ident) is None:
            raise NotDeclaredException.NotDeclaredException(self.ident, False, self.no_line, self.pos)
        elif env.get_variable_type(self.ident).type != "int":
            raise SyntaxException("Increment can be applied only to integers, but got "
                                                  + str(env.get_variable_type(self.ident))
                                                  + " for variable " + self.ident + ".", self.no_line)

    def generate_body(self, env):
        return "iinc " + str(env.get_variable_value(self.ident)) + " 1\n"