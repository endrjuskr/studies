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
invokestatic MyClass.p()V
ldc 1 
invokestatic Runtime.printInt(I)V
return
.end method 
.method public static p()V
.limit stack 100
.limit locals 1
return
.end method 
