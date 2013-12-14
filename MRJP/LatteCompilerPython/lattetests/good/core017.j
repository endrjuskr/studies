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
ldc 4 
istore 1
iconst_1
invokestatic MyClass.printBool(I)V
iconst_1
iconst_1
if_icmpeq cmp_11_164_t
goto cmp_11_164_f
cmp_11_164_t:
iconst_1 
goto cmp_11_164
cmp_11_164_f:
iconst_0 
cmp_11_164:
dup
ifne or_11_164
ldc 1 
invokestatic MyClass.dontCallMe(I)I
ior 
or_11_164:
invokestatic MyClass.printBool(I)V
ldc 4 
ldc 5 
ineg
if_icmplt cmp_12_208_t
goto cmp_12_208_f
cmp_12_208_t:
iconst_1 
goto cmp_12_208
cmp_12_208_f:
iconst_0 
cmp_12_208:
dup
ifeq and_12_208
ldc 2 
invokestatic MyClass.dontCallMe(I)I
iand 
and_12_208:
invokestatic MyClass.printBool(I)V
ldc 4 
iload 1
if_icmpeq cmp_14_247_t
goto cmp_14_247_f
cmp_14_247_t:
iconst_1 
goto cmp_14_247
cmp_14_247_f:
iconst_0 
cmp_14_247:
dup
ifeq and_14_247
iconst_1
iconst_0
iconst_1
ixor
if_icmpeq cmp_14_257_t
goto cmp_14_257_f
cmp_14_257_t:
iconst_1 
goto cmp_14_257
cmp_14_257_f:
iconst_0 
cmp_14_257:
dup
ifeq and_14_257
iconst_1
iand 
and_14_257:
iand 
and_14_247:
invokestatic MyClass.printBool(I)V
iconst_0
iconst_0
invokestatic MyClass.implies(II)I
invokestatic MyClass.printBool(I)V
iconst_0
iconst_1
invokestatic MyClass.implies(II)I
invokestatic MyClass.printBool(I)V
iconst_1
iconst_0
invokestatic MyClass.implies(II)I
invokestatic MyClass.printBool(I)V
iconst_1
iconst_1
invokestatic MyClass.implies(II)I
invokestatic MyClass.printBool(I)V
return
.end method 
.method public static dontCallMe(I)I
.limit stack 100
.limit locals 2
iload 0
invokestatic Runtime.printInt(I)V
iconst_1
ireturn 
.end method 
.method public static printBool(I)V
.limit stack 100
.limit locals 2
iload 0
ifeq condelse_30_527_f
ldc "true" 
invokestatic Runtime.printString(Ljava/lang/String;)V
goto condelse_30_527
condelse_30_527_f:
ldc "false" 
invokestatic Runtime.printString(Ljava/lang/String;)V
condelse_30_527:
return 
.end method 
.method public static implies(II)I
.limit stack 100
.limit locals 3
iload 0
iconst_1
ixor
dup
ifne or_39_0
iload 0
iload 1
if_icmpeq cmp_39_668_t
goto cmp_39_668_f
cmp_39_668_t:
iconst_1 
goto cmp_39_668
cmp_39_668_f:
iconst_0 
cmp_39_668:
ior 
or_39_0:
ireturn 
.end method 
