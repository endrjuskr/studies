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
ldc 17 
invokestatic MyClass.ev(I)I
invokestatic Runtime.printInt(I)V
return
.end method 
.method public static ev(I)I
.limit stack 100
.limit locals 2
iload 0
ldc 0 
if_icmpgt cmp_9_122_t
goto cmp_9_122_f
cmp_9_122_t:
iconst_1 
goto cmp_9_122
cmp_9_122_f:
iconst_0 
cmp_9_122:
ifeq condelse_9_118_f
iload 0
ldc 2 
isub 
invokestatic MyClass.ev(I)I
ireturn 
goto condelse_9_118
condelse_9_118_f:
iload 0
ldc 0 
if_icmplt cmp_12_166_t
goto cmp_12_166_f
cmp_12_166_t:
iconst_1 
goto cmp_12_166
cmp_12_166_f:
iconst_0 
cmp_12_166:
ifeq condelse_12_162_f
ldc 0 
ireturn 
goto condelse_12_162
condelse_12_162_f:
ldc 1 
ireturn 
condelse_12_162:
condelse_9_118:
return
.end method 
