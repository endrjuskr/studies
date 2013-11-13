__author__ = 'andrzejskrodzki'


class TypeException(BaseException):

    def __init__(self, expected_type, received_type, no_line):
        self.expected_type = expected_type
        self.received_type = received_type
        self.no_line = no_line

    def __str__(self):
        return "Type Error: Expected type is " + str(self.expected_type) + ", but " \
               + str(self.received_type) + " was received at line - " + str(self.no_line) + "."