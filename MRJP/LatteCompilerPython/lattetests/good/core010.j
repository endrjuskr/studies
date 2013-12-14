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
ldc 5 
invokestatic MyClass.fac(I)I
invokestatic Runtime.printInt(I)V
return
.end method 
.method public static fac(I)I
.limit stack 100
.limit locals 4
iconst_0 
istore 1
iconst_0 
istore 2
ldc 1 
istore 1
iload 0
istore 2
while_13_150_w:
iload 2
ldc 0 
if_icmpgt cmp_13_157_t
goto cmp_13_157_f
cmp_13_157_t:
iconst_1 
goto cmp_13_157
cmp_13_157_f:
iconst_0 
cmp_13_157:
ifeq while_13_150
iload 1
iload 2
imul
istore 1
iload 2
ldc 1 
isub 
istore 2
goto while_13_150_w
while_13_150:
iload 1
ireturn 
.end method 
