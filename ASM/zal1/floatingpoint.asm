;;; Andrzej Skrodzki 292510

SYS_WRITE equ 1
SYS_EXIT  equ 60
POS_SIGN  equ 63
POS_EX    equ 52

section .bss
    	a:   			resq    1
    	b:	 			resq	1
    	significanta:	resq	1
    	significantb:	resq	1
    	exp:			resb	1
    	signa 			resb	1

section .text
        			global plus, _start
get_significant:	; Gets significant from number which is represented by bits 52..0
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, POS_EX
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					mov rbx, 1
					shl rbx, POS_EX
					or  rax, rbx    ; Add 1 to number
					leave
					ret
get_exp:			; Gets exponential from number which is represented by bits 63..53 with added 1023
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, 12
					sub rbx, 1 
					shr rbx, POS_EX
					and rax, rbx 		; Collect bits 63..53
					leave
					ret
get_sing:			; Gets sign of number which is represented by bit 64
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					shr rbx, POS_SIGN
					leave
					ret
plus:
					enter 0, 0
assigna:			mov qword [a], rax
assignb:			mov qword [b], rbx
countsiga:			push [a]
					call get_exp
					mov [significanta], rax
countexpa:			push [a]
					call get_exp
					mov rcx, rax
countexpb			push [b]
					call get_exp
					mov rdx, rax
					cmp rcx, rdx
					je expeq	; Exponents are the same
					jg expgt	; Exponent of a is greater
					jl explt	; Exponent of b is greater 
expeq:				mov [exp], rcx
					jmp countsigna
expgt:				mov [exp], rcx
					sub rcx, rdx
					shr [significantb], rcx
					jmp countsiga
explt:				mov [exp], rdx
					sub rdx, rcx
					shr [significanta], rdx
countsigna:			push [a]
					call get_sign
					mov rcx, rax
countsignb:			push [b]
					call get_sign
					mov rdx, rax
					mov [signa], rcx
compsign			cmp rcx, rdx
					je sames	; same signs so act as add
					jneq difs	; different sign so act as sub
sames:				add [significanta], [significantb]
					jmp normalize
difs:				sub [significanta], [significantb]
normalize:			mov rax, 1
					shl rax, POS_EX
					cmp [significanta], rax
					jl  normalizer
					jg  normalizel
					jmp rets
normalizer:			mov rcx, 1
					shl rcx, POS_EX
					mov rdx, rcx
					and rcx, [significanta]
					cmp rcx, rdx
					je rets
					cmp [exp], 0
					jnq decrease exp
					mov [signicanta], 0
					jmp rets
decreaseexp:		sub [exp], 1
					shl [significanta], 1
					jmp normalizer
normalizel:			mov rcx, [significanta]
					shr rcx, POS_EX
					cmp rcx, 1
					je rets
					cmp [exp], 2047
					jnq increaseexp
					mov [significanta], 0
					jmp rets
increaseexp:		shr [significanta], 1
					add [exp], 1
					jmp normalizel
rets:				mov eax, [signa]
					shl eax, 11
					add eax, [exp]
					shl eax, POS_EXP
					add eax, [significanta]
					leave
					ret

minus:
					enter 0, 0
					mul rbx, -1
					call plus
					leave
					ret
