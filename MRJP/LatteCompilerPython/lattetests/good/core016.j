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
ldc 17 
istore 1
while_5_73_w:
iload 1
ldc 0 
if_icmpgt cmp_5_80_t
goto cmp_5_80_f
cmp_5_80_t:
iconst_1 
goto cmp_5_80
cmp_5_80_f:
iconst_0 
cmp_5_80:
ifeq while_5_73
iload 1
ldc 2 
isub 
istore 1
goto while_5_73_w
while_5_73:
iload 1
ldc 0 
if_icmplt cmp_7_108_t
goto cmp_7_108_f
cmp_7_108_t:
iconst_1 
goto cmp_7_108
cmp_7_108_f:
iconst_0 
cmp_7_108:
ifeq condelse_7_104_f
ldc 0 
invokestatic Runtime.printInt(I)V
return
goto condelse_7_104
condelse_7_104_f:
ldc 1 
invokestatic Runtime.printInt(I)V
return
condelse_7_104:
return
.end method 
