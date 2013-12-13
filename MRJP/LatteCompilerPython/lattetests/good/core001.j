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
ldc 10 
invokestatic MyClass.fac(I)I
invokestatic Runtime.printInt(I)V
ldc 10 
invokestatic MyClass.rfac(I)I
invokestatic Runtime.printInt(I)V
ldc 10 
invokestatic MyClass.mfac(I)I
invokestatic Runtime.printInt(I)V
ldc 10 
invokestatic MyClass.ifac(I)I
invokestatic Runtime.printInt(I)V
ldc "" 
astore 0
ldc 10 
istore 1
ldc 1 
istore 2
while_10_181_w:
iload 1
ldc 0 
if_icmpgt cmp_10_188_t
goto cmp_10_188_f
cmp_10_188_t:
iconst_1 
goto cmp_10_188
cmp_10_188_f:
iconst_0 
cmp_10_188:
ifeq while_10_181
iload 2
iload 1
imul
istore 2
iinc 1 -1
goto while_10_181_w
while_10_181:
iload 2
invokestatic Runtime.printInt(I)V
ldc "=" 
ldc 60 
invokestatic MyClass.repStr(Ljava/lang/String;I)Ljava/lang/String;
invokestatic Runtime.printString(Ljava/lang/String;)V
ldc "hello */" 
invokestatic Runtime.printString(Ljava/lang/String;)V
ldc "/* world" 
invokestatic Runtime.printString(Ljava/lang/String;)V
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
while_28_413_w:
iload 2
ldc 0 
if_icmpgt cmp_28_420_t
goto cmp_28_420_f
cmp_28_420_t:
iconst_1 
goto cmp_28_420
cmp_28_420_f:
iconst_0 
cmp_28_420:
ifeq while_28_413
iload 1
iload 2
imul
istore 1
iload 2
ldc 1 
isub 
istore 2
goto while_28_413_w
while_28_413:
iload 1
ireturn 
.end method 
.method public static rfac(I)I
.limit stack 100
.limit locals 2
iload 0
ldc 0 
if_icmpeq cmp_36_497_t
goto cmp_36_497_f
cmp_36_497_t:
iconst_1 
goto cmp_36_497
cmp_36_497_f:
iconst_0 
cmp_36_497:
ifeq condelse_36_493_f
ldc 1 
ireturn 
goto condelse_36_493
condelse_36_493_f:
iload 0
iload 0
ldc 1 
isub 
invokestatic MyClass.rfac(I)I
imul
ireturn 
condelse_36_493:
iconst_0 
pop 
.end method 
.method public static mfac(I)I
.limit stack 100
.limit locals 2
iload 0
ldc 0 
if_icmpeq cmp_43_575_t
goto cmp_43_575_f
cmp_43_575_t:
iconst_1 
goto cmp_43_575
cmp_43_575_f:
iconst_0 
cmp_43_575:
ifeq condelse_43_571_f
ldc 1 
ireturn 
goto condelse_43_571
condelse_43_571_f:
iload 0
iload 0
ldc 1 
isub 
invokestatic MyClass.nfac(I)I
imul
ireturn 
condelse_43_571:
iconst_0 
pop 
.end method 
.method public static nfac(I)I
.limit stack 100
.limit locals 2
iload 0
ldc 0 
if_icmpne cmp_50_653_t
goto cmp_50_653_f
cmp_50_653_t:
iconst_1 
goto cmp_50_653
cmp_50_653_f:
iconst_0 
cmp_50_653:
ifeq condelse_50_649_f
iload 0
ldc 1 
isub 
invokestatic MyClass.mfac(I)I
iload 0
imul
ireturn 
goto condelse_50_649
condelse_50_649_f:
ldc 1 
ireturn 
condelse_50_649:
iconst_0 
pop 
.end method 
.method public static ifac(I)I
.limit stack 100
.limit locals 2
ldc 1 
iload 0
invokestatic MyClass.ifac2f(II)I
ireturn 
.end method 
.method public static ifac2f(II)I
.limit stack 100
.limit locals 4
iload 0
iload 1
if_icmpeq cmp_59_788_t
goto cmp_59_788_f
cmp_59_788_t:
iconst_1 
goto cmp_59_788
cmp_59_788_f:
iconst_0 
cmp_59_788:
ifeq cond_59_784
iload 0
ireturn 
cond_59_784:
iload 0
iload 1
if_icmpgt cmp_61_828_t
goto cmp_61_828_f
cmp_61_828_t:
iconst_1 
goto cmp_61_828
cmp_61_828_f:
iconst_0 
cmp_61_828:
ifeq cond_61_824
ldc 1 
ireturn 
cond_61_824:
iconst_0 
istore 2
iload 0
iload 1
iadd 
ldc 2 
idiv 
istore 2
iload 0
iload 2
invokestatic MyClass.ifac2f(II)I
iload 2
ldc 1 
iadd 
iload 1
invokestatic MyClass.ifac2f(II)I
imul
ireturn 
.end method 
.method public static repStr(Ljava/lang/String;I)Ljava/lang/String;
.limit stack 100
.limit locals 5
ldc "" 
astore 2
ldc 0 
istore 3
while_71_1007_w:
iload 3
iload 1
if_icmplt cmp_71_1013_t
goto cmp_71_1013_f
cmp_71_1013_t:
iconst_1 
goto cmp_71_1013
cmp_71_1013_f:
iconst_0 
cmp_71_1013:
ifeq while_71_1007
aload 2
aload 0
invokestatic Runtime.concatenateString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
astore 2
iinc 3 1
goto while_71_1007_w
while_71_1007:
aload 2
areturn 
.end method 
