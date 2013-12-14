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
ldc "&&" 
invokestatic Runtime.printString(Ljava/lang/String;)V
ldc 1 
ineg
invokestatic MyClass.test(I)I
dup
ifeq and_5_77
ldc 0 
invokestatic MyClass.test(I)I
iand 
and_5_77:
invokestatic MyClass.printBool(I)V
ldc 2 
ineg
invokestatic MyClass.test(I)I
dup
ifeq and_6_111
ldc 1 
invokestatic MyClass.test(I)I
iand 
and_6_111:
invokestatic MyClass.printBool(I)V
ldc 3 
invokestatic MyClass.test(I)I
dup
ifeq and_7_145
ldc 5 
ineg
invokestatic MyClass.test(I)I
iand 
and_7_145:
invokestatic MyClass.printBool(I)V
ldc 234234 
invokestatic MyClass.test(I)I
dup
ifeq and_8_179
ldc 21321 
invokestatic MyClass.test(I)I
iand 
and_8_179:
invokestatic MyClass.printBool(I)V
ldc "||" 
invokestatic Runtime.printString(Ljava/lang/String;)V
ldc 1 
ineg
invokestatic MyClass.test(I)I
dup
ifne or_10_242
ldc 0 
invokestatic MyClass.test(I)I
ior 
or_10_242:
invokestatic MyClass.printBool(I)V
ldc 2 
ineg
invokestatic MyClass.test(I)I
dup
ifne or_11_276
ldc 1 
invokestatic MyClass.test(I)I
ior 
or_11_276:
invokestatic MyClass.printBool(I)V
ldc 3 
invokestatic MyClass.test(I)I
dup
ifne or_12_310
ldc 5 
ineg
invokestatic MyClass.test(I)I
ior 
or_12_310:
invokestatic MyClass.printBool(I)V
ldc 234234 
invokestatic MyClass.test(I)I
dup
ifne or_13_344
ldc 21321 
invokestatic MyClass.test(I)I
ior 
or_13_344:
invokestatic MyClass.printBool(I)V
ldc "!" 
invokestatic Runtime.printString(Ljava/lang/String;)V
iconst_1
invokestatic MyClass.printBool(I)V
iconst_0
invokestatic MyClass.printBool(I)V
return
.end method 
.method public static printBool(I)V
.limit stack 100
.limit locals 2
iload 0
iconst_1
ixor
ifeq condelse_22_480_f
ldc "false" 
invokestatic Runtime.printString(Ljava/lang/String;)V
goto condelse_22_480
condelse_22_480_f:
ldc "true" 
invokestatic Runtime.printString(Ljava/lang/String;)V
condelse_22_480:
return 
.end method 
.method public static test(I)I
.limit stack 100
.limit locals 2
iload 0
invokestatic Runtime.printInt(I)V
iload 0
ldc 0 
if_icmpgt cmp_32_613_t
goto cmp_32_613_f
cmp_32_613_t:
iconst_1 
goto cmp_32_613
cmp_32_613_f:
iconst_0 
cmp_32_613:
ireturn 
.end method 
