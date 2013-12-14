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
ldc 78 
istore 1
ldc 1 
istore 2
iload 2
invokestatic Runtime.printInt(I)V
iload 1
invokestatic Runtime.printInt(I)V
while_8_84_w:
iload 1
ldc 76 
if_icmpgt cmp_8_91_t
goto cmp_8_91_f
cmp_8_91_t:
iconst_1 
goto cmp_8_91
cmp_8_91_f:
iconst_0 
cmp_8_91:
ifeq while_8_84
iinc 1 -1
iload 1
invokestatic Runtime.printInt(I)V
iload 1
ldc 7 
iadd 
istore 2
iload 2
invokestatic Runtime.printInt(I)V
goto while_8_84_w
while_8_84:
iload 1
invokestatic Runtime.printInt(I)V
iload 1
ldc 4 
if_icmpgt cmp_17_270_t
goto cmp_17_270_f
cmp_17_270_t:
iconst_1 
goto cmp_17_270
cmp_17_270_f:
iconst_0 
cmp_17_270:
ifeq condelse_17_266_f
ldc 4 
istore 2
iload 2
invokestatic Runtime.printInt(I)V
goto condelse_17_266
condelse_17_266_f:
ldc "foo" 
invokestatic Runtime.printString(Ljava/lang/String;)V
condelse_17_266:
iload 1
invokestatic Runtime.printInt(I)V
return
.end method 
