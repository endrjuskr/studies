__author__ = 'Andrzej Skrodzki - as292510'

__all__ = ["FunType", "Type"]

from operator import eq


class Type(object):
    def __init__(self, type):
        self.type = type
        self.dict = {}
        self.fill_matches()

    def __eq__(self, other):
        return self.type == other.type

    def __ne__(self, other):
        return self.type != other.type

    def __str__(self):
        return self.type

    def is_function(self):
        return False

    def fill_matches(self):
        self.dict["int"] = "I"
        self.dict["string"] = "Ljava/lang/String;"
        self.dict["void"] = "V"
        self.dict["boolean"] = "I"

    def generate_code_jvm(self):
        return self.dict[self.type]


class ArrayType(Type):
    def __init__(self, array_type, size):
        super(ArrayType, self).__init__("arraytype")
        self.size = size
        self.array_type = array_type

    def get_length(self, env):
        if self.size.get_value() is None:
            pass
        else:
            return self.size.get_value()


class FunType(Type):
    def __init__(self, return_type, params_types):
        super(FunType, self).__init__("funtype")
        self.return_type = return_type
        self.params_types = params_types

    def __eq__(self, other):
        return self.return_type == other.return_type and len(self.params_types) == len(other.params_types) and all(
            map(eq, self.params_types, other.params_types))

    def __str__(self):
        return "(" + str(self.return_type) + ", " + str(self.params_types) + ")"

    def is_function(self):
        return True

    def generate_code_jvm(self):
        s = "("
        for t in self.params_types:
            s += t.generate_code_jvm()

        s += ")" + self.return_type.generate_code_jvm()
        return s


