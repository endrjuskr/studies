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
ldc 56 
istore 1
iload 1
ldc 45 
iadd 
ldc 2 
if_icmple cmp_6_98_t
goto cmp_6_98_f
cmp_6_98_t:
iconst_1 
goto cmp_6_98
cmp_6_98_f:
iconst_0 
cmp_6_98:
ifeq condelse_6_94_f
ldc 1 
istore 0
goto condelse_6_94
condelse_6_94_f:
ldc 2 
istore 0
condelse_6_94:
iload 0
invokestatic Runtime.printInt(I)V
return
.end method 
