__author__ = 'Andrzej Skrodzki - as292510'

from LatteBaseException import LatteBaseException


class TypeException(LatteBaseException):
    def __init__(self, expected_type, received_type, no_line, pos):
        super(TypeException, self).__init__(no_line, pos)
        self.expected_type = expected_type
        self.received_type = received_type

    def __str__(self):
        return super(TypeException, self).__str__() \
               + "Type Error: Expected type is " + str(self.expected_type) + ", but " \
               + str(self.received_type) + " was received."