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
    	exp:			resq	1
    	signa 			resq	1

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
get_sign:			; Gets sign of number which is represented by bit 64
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					shr rbx, POS_SIGN
					leave
					ret
plus:
					enter 0, 0
assigna:			mov qword [a], rax
assignb:			mov qword [b], rbx
countsiga:			push qword [a]
					call get_exp
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
					shl rax, POS_EX
					cmp qword [significanta], rax
					jl  normalizer
					jg  normalizel
					jmp rets
normalizer:			mov rcx, 1
					shl rcx, POS_EX
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
					shr rcx, POS_EX
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
					shl rax, 11
					add rax, qword [exp]
					shl rax, POS_EX
					add rax, qword [significanta]
					leave
					ret

minus:
					enter 0, 0
					imul rbx, -1
					call plus
					leave
					ret
