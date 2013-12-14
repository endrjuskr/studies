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
invokestatic Runtime.readInt()I
istore 1
invokestatic Runtime.readString()Ljava/lang/String;
astore 2
invokestatic Runtime.readString()Ljava/lang/String;
astore 3
iload 1
ldc 5 
isub 
invokestatic Runtime.printInt(I)V
aload 2
aload 3
invokestatic Runtime.concatenateString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
invokestatic Runtime.printString(Ljava/lang/String;)V
return
.end method 
