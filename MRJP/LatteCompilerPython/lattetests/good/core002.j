.class public MyClass
.super java/lang/Object 
                 .method public <init>()V 
                 aload_0 
                 invokespecial java/lang/Object/<init>()V 
                 return 
                 .end method 
.method public static main([Ljava/lang/String;)V 
.limit stack 100
.limit locals 1
invokestatic MyClass.foo()V
return
.end method 
.method public static foo()V
.limit stack 100
.limit locals 1
ldc "foo" 
invokestatic Runtime.printString(Ljava/lang/String;)V
return 
.end method 
