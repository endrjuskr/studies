;;; Andrzej Skrodzki 292510

SYS_WRITE equ 1
SYS_EXIT  equ 60

	SECTION .data		; data section
		msg1:	db "Hello World1",10	; the string to print, 10=cr
		len1:	equ $-msg1
		msg2:	db "Hello World2",10	; the string to print, 10=cr
		len2:	equ $-msg2
		msg3:	db "Hello World3",10	; the string to print, 10=cr
		len3:	equ $-msg3
		msg4:	db "Hello World4",10	; the string to print, 10=cr
		len4:	equ $-msg4
		msg5:	db "Hello World5",10	; the string to print, 10=cr
		len5:	equ $-msg5

section .bss
    	a:   			resq    1
    	b:	 			resq	1
    	significanta:	resq	1
    	significantb:	resq	1
    	exp:			resq	1
    	signa: 			resq	1
    	signb: 			resq	1
    	expa: 			resq	1
    	expb: 			resq	1

section .text
        			global plus
        			extern get_sign, get_exp, get_significant, prepare_significant, LEN_EX, LEN_SIG
plus:
					enter 0, 0
assigna:			mov qword [a], rax
assignb:			mov qword [b], rbx
countsigna:			push qword [a]
					call get_sign
					mov qword [signa], rax
countsignb:			push qword [b]
					call get_sign
					mov qword [signb], rax	
countsiga:			push qword [a]
					call get_significant
					mov qword [significanta], rax					
countsigb:			push qword [b]
					call get_significant
					mov qword [significantb], rax
countexpa:			push qword [a]
					call get_exp
					mov qword [expa], rax					
countexpb:			push qword [b]
					call get_exp
					mov qword [expb], rax
checka0:			cmp qword [expa], 0
					jne checkb0
					mov rax, qword[b]
					jmp leavep 
checkb0:			cmp qword [expb], 0
					jne checkamax
					mov rax, qword[a]
					jmp leavep
checkamax:			cmp qword [expa], 2047
					jne checkbmax
					mov rax, qword [expa]
					mov rbx, qword [expb]
					cmp rax, rbx
					jne onlyonemax
					mov rax, qword [signa]
					mov rbx, qword [signb]
					cmp rax, rbx
					je onlyonemax
					mov rax, qword [expa]
					mov qword [exp], rax
					mov qword [significanta], 1
					jmp ret2
onlyonemax:			mov rax, qword [a]
					jmp leavep 
checkbmax:			cmp qword [expb], 2047
					jne compexp
					mov rax, qword[b]
					jmp leavep
compexp:			mov rdx, qword [expb]
					mov rcx, qword [expa]
					cmp rcx, rdx
					je expeq	; Exponents are the same
					jg expgt	; Exponent of a is greater
					jl explt	; Exponent of b is greater 
expeq:				mov rcx, qword [expa]
					mov qword [exp], rcx					
					jmp compsign
expgt:				mov rcx, qword [expa]
					mov qword [exp], rcx
					sub qword [expb], rcx
shiftb:				cmp qword[expb], 0
					je compsign
					shr qword [significantb], 1
					add qword [expb], 1
					jmp shiftb  
explt:				mov rdx, qword [expb]
					mov qword [exp], rdx
					sub qword [expa], rdx
shifta:				cmp qword [expa], 0
					je compsign
					shr qword [significanta], 1
					add qword[expa], 1
					jmp shifta 
compsign:			mov rdx, qword [signb]
					mov rcx, qword [signa]
					cmp rcx, rdx
					jne difs	; different sign so act as sub
					je sames
sames:				mov rax, qword [significantb]
					add qword [significanta], rax
					jmp normalize
difs:				mov rax, qword [significantb]
					sub qword [significanta], rax
normalize:			mov rax, 1
					shl rax, LEN_SIG
					cmp qword [significanta], rax
					jl  normalizer
					jg  normalizel
					je rets
normalizer:			cmp qword [exp], 0
					jne decreaseexp
					mov qword [significanta], 0
					jmp rets
decreaseexp:		mov rcx, 1
					shl rcx, LEN_SIG
					mov rdx, rcx
					and rcx, qword [significanta]
					cmp rcx, rdx
					je rets
					sub qword [exp], 1
					shl qword [significanta], 1
					jmp normalizer
normalizel:			cmp qword [exp], 2047
					jne increaseexp
					je setsig
setsig:				mov qword [significanta], 0
					jmp ret2
increaseexp:		mov rcx, qword [significanta]
					shr rcx, LEN_SIG
					cmp rcx, 1
					je rets
					shr qword [significanta], 1
					add qword [exp], 1
					jmp normalizel
rets:				push qword [significanta]
					call prepare_significant
					mov qword [significanta], rax
ret2:				mov rax, qword [signa]
					shl rax, LEN_EX
					add rax, qword [exp]
					shl rax, LEN_SIG
					add rax, qword [significanta]
leavep:				leave
					ret
