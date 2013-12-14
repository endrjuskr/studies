.class public MyClass
.super java/lang/Object 
                 .method public <init>()V 
                 aload_0 
                 invokespecial java/lang/Object/<init>()V 
                 return 
                 .end method 
.method public static main([Ljava/lang/String;)V 
.limit stack 100
.limit locals 2
invokestatic MyClass.foo()I
istore 0
iload 0
invokestatic Runtime.printInt(I)V
return
.end method 
.method public static foo()I
.limit stack 100
.limit locals 1
ldc 10 
ireturn 
.end method 
