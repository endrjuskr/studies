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
iconst_1
if_icmpeq cmp_4_52_t
goto cmp_4_52_f
cmp_4_52_t:
iconst_1 
goto cmp_4_52
cmp_4_52_f:
iconst_0 
cmp_4_52:
ifeq cond_4_48
ldc 42 
invokestatic Runtime.printInt(I)V
cond_4_48:
return
.end method 
