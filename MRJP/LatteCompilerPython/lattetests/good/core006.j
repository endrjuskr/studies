.class public MyClass
.super java/lang/Object 
                 .method public <init>()V 
                 aload_0 
                 invokespecial java/lang/Object/<init>()V 
                 return 
                 .end method 
.method public static main([Ljava/lang/String;)V 
.limit stack 100
.limit locals 3
iconst_0 
istore 0
iconst_0 
istore 1
ldc 45 
istore 0
ldc 36 
ineg 
istore 1
iload 0
invokestatic Runtime.printInt(I)V
iload 1
invokestatic Runtime.printInt(I)V
return
.end method 
