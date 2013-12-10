__author__ = 'andrzejskrodzki'


class Type(object):
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return self.type == other.type

    def __ne__(self, other):
        return self.type != other.type

    def __str__(self):
        return self.type

    def isFunction(self):
        return False

