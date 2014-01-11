__author__ = 'Andrzej Skrodzki - as292510'


from Type import Type


class ArrayType(Type):
    def __init__(self, array_type, size):
        super(ArrayType, self).__init__("arraytype")
        self.size = size
        self.array_type = array_type

    def get_length(self, env):
        if self.size.get_value() is None:

        else:
            return self.size.get_value()