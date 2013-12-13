__author__ = 'Andrzej Skrodzki - as292510'


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

    def isFunction(self):
        return False

    def fill_matches(self):
        self.dict["int"] = "I"
        self.dict["string"] = "Ljava/lang/String;"
        self.dict["void"] = "V"
        self.dict["boolean"] = "Z"

    def generate_code(self):
        return self.dict[self.type]

