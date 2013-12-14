.class public MyClass
.super java/lang/Object 
                 .method public <init>()V 
                 aload_0 
                 invokespecial java/lang/Object/<init>()V 
                 return 
                 .end method 
.method public static main([Ljava/lang/String;)V 
.limit stack 100
.limit locals 5
iconst_0 
istore 1
iconst_0 
istore 2
iconst_0 
istore 3
ldc 1 
istore 1
iload 1
istore 2
ldc 5000000 
istore 3
iload 1
invokestatic Runtime.printInt(I)V
while_9_108_w:
iload 2
iload 3
if_icmplt cmp_9_115_t
goto cmp_9_115_f
cmp_9_115_t:
iconst_1 
goto cmp_9_115
cmp_9_115_f:
iconst_0 
cmp_9_115:
ifeq while_9_108
iload 2
invokestatic Runtime.printInt(I)V
iload 1
iload 2
iadd 
istore 2
iload 2
iload 1
isub 
istore 1
goto while_9_108_w
while_9_108:
return
.end method 
