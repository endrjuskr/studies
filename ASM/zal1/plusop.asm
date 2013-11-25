;;; Andrzej Skrodzki 292510

SYS_WRITE equ 1
SYS_EXIT  equ 60

section .data

section .bss
    	a:   			resq    1
    	b:	 			resq	1
    	significanta:	resq	1
    	significantb:	resq	1
    	exp:			resq	1
    	signa 			resq	1

section .text
        			global plus
        			extern get_sign, get_exp, get_significant, LEN_EX, LEN_SIG
plus:
					enter 0, 0
assigna:			mov qword [a], rax
assignb:			mov qword [b], rbx
countsiga:			push qword [a]
					call get_sign
					mov qword [signa], rax
countexpa:			push qword [a]
					call get_exp
					mov rcx, rax
countexpb			push qword [b]
					call get_exp
					mov rdx, rax
					cmp rcx, rdx
					je expeq	; Exponents are the same
					jg expgt	; Exponent of a is greater
					jl explt	; Exponent of b is greater 
expeq:				mov qword [exp], rcx
					jmp countsigna
expgt:				mov qword [exp], rcx
					sub rcx, rdx
shiftb:				cmp rcx, 0
					je countsiga
					shr qword [significantb], 1
					sub rcx, 1
					jmp shiftb  
explt:				mov qword [exp], rdx
					sub rdx, rcx
shifta:				cmp rdx, 0
					je countsiga
					shr qword [significanta], 1
					sub rdx, 1
					jmp shifta 
countsigna:			push qword [a]
					call get_sign
					mov rcx, rax
countsignb:			push qword [b]
					call get_sign
					mov rdx, rax
					mov qword [signa], rcx
compsign			cmp rcx, rdx
					jne difs	; different sign so act as sub
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
					jmp rets
normalizer:			mov rcx, 1
					shl rcx, LEN_SIG
					mov rdx, rcx
					and rcx, qword [significanta]
					cmp rcx, rdx
					je rets
					cmp qword [exp], 0
					jne decreaseexp
					mov qword [significanta], 0
					jmp rets
decreaseexp:		sub qword [exp], 1
					shl qword [significanta], 1
					jmp normalizer
normalizel:			mov rcx, qword [significanta]
					shr rcx, LEN_SIG
					cmp rcx, 1
					je rets
					cmp qword [exp], 2047
					jne increaseexp
					mov qword [significanta], 0
					jmp rets
increaseexp:		shr qword [significanta], 1
					add qword [exp], 1
					jmp normalizel
rets:				mov rax, qword [signa]
					shl rax, LEN_EX
					add rax, qword [exp]
					shl rax, LEN_SIG
					add rax, qword [significanta]
					leave
					ret
