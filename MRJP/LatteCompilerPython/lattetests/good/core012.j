.class public MyClass
.super java/lang/Object 
                 .method public <init>()V 
                 aload_0 
                 invokespecial java/lang/Object/<init>()V 
                 return 
                 .end method 
.method public static main([Ljava/lang/String;)V 
.limit stack 100
.limit locals 4
ldc 56 
istore 1
ldc 23 
ineg
istore 2
iload 1
iload 2
iadd 
invokestatic Runtime.printInt(I)V
iload 1
iload 2
isub 
invokestatic Runtime.printInt(I)V
iload 1
iload 2
imul
invokestatic Runtime.printInt(I)V
ldc 45 
ldc 2 
idiv
invokestatic Runtime.printInt(I)V
ldc 78 
ldc 3 
irem
invokestatic Runtime.printInt(I)V
iload 1
iload 2
isub 
iload 1
iload 2
iadd 
if_icmpgt cmp_11_197_t
goto cmp_11_197_f
cmp_11_197_t:
iconst_1 
goto cmp_11_197
cmp_11_197_f:
iconst_0 
cmp_11_197:
invokestatic MyClass.printBool(Z)V
iload 1
iload 2
idiv
iload 1
iload 2
imul
if_icmple cmp_12_223_t
goto cmp_12_223_f
cmp_12_223_t:
iconst_1 
goto cmp_12_223
cmp_12_223_f:
iconst_0 
cmp_12_223:
invokestatic MyClass.printBool(Z)V
ldc "string" 
ldc " " 
invokestatic Runtime.concatenateString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
ldc "concatenation" 
invokestatic Runtime.concatenateString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
invokestatic Runtime.printString(Ljava/lang/String;)V
return
.end method 
.method public static printBool(Z)V
.limit stack 100
.limit locals 2
iload 0
ifeq condelse_18_331_f
ldc "true" 
invokestatic Runtime.printString(Ljava/lang/String;)V
return 
goto condelse_18_331
condelse_18_331_f:
ldc "false" 
invokestatic Runtime.printString(Ljava/lang/String;)V
return 
condelse_18_331:
return
.end method 
