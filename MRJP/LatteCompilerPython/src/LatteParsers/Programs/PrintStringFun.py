__author__ = 'Andrzej Skrodzki - as292510'


from PredefinedFun import PredefinedFun
from LatteParsers.Types.Type import Type

class PrintStringFun(PredefinedFun):
    def __init__(self):
        super(PrintStringFun, self).__init__(Type("void"), "error", [Type("string")])


    def generate_body(self):
        return ".limit stack 2 \n \
                getstatic java/lang/System/out Ljava/io/PrintStream; \n \
                aload_0 \n \
                invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V \n \
                return \n"