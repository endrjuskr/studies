__author__ = 'Andrzej Skrodzki - as292510'

from PredefinedFun import PredefinedFun
from LatteParsers.Types.Type import Type

class ErrorFun(PredefinedFun):
    def __init__(self):
        super(ErrorFun, self).__init__(Type("void"), "error", [])

    def type_check(self):
        pass