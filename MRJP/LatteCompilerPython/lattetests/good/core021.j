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
iconst_1
ifeq cond_2_17
ldc 1 
invokestatic Runtime.printInt(I)V
return
cond_2_17:
return
.end method 
