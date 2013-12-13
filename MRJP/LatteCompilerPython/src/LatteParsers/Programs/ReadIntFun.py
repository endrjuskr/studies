__author__ = 'Andrzej Skrodzki - as292510'


from PredefinedFun import PredefinedFun
from LatteParsers.Types.Type import Type

class ReadIntFun(PredefinedFun):
    def __init__(self):
        super(ReadIntFun, self).__init__(Type("int"), "error", [])

    def generate_body(self):
        return ".limit stack 5 \n \
                .limit locals 100 \n \
                ldc 0 \n \
                istore 50 \n \
                Label1: \n \
                getstatic java/lang/System/in Ljava/io/InputStream;\n \
                invokevirtual java/io/InputStream/read()I \n \
                istore 51 \n \
                iload 51  \n \
                ldc 10  \n \
                isub  \n \
                ifeq Label2  \n \
                iload 51  \n \
                ldc 32  \n \
                isub  \n \
                ifeq Label2  \n \
                iload 51  \n \
                ldc 48  \n \
                isub  \n \
                ldc 10  \n \
                iload 50  \n \
                imul  \n \
                iadd  \n \
                istore 50  \n \
                goto Label1  \n \
                Label2:  \n \
                iload 50  \n"