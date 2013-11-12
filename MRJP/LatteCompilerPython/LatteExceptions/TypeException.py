__author__ = 'andrzejskrodzki'

class TypeEception(Exception):
    def __init__(self, expected_type, received_type):
        self.expected_type = expected_type
        self.received_type = received_type

    def __str__(self):
        return "Type Error: Expected type is " + self.expected_type + ", but " + self.received_type + " was received."