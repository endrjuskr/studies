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
        			extern get_sign, get_exp, get_significant, prepare_significant, LEN_EX, LEN_SIG, LEN_SIG_EX, LEN_SIG_EXT
plus:
					enter 0, 0
assigna:			mov qword [a], rax				; assigning first number to a
assignb:			mov qword [b], rbx  			; assigning second number to b

countsigna:			push qword [a]					; counting sign of number a
					call get_sign
					mov qword [signa], rax			; assigning sign of a to signa
countsignb:			push qword [b]					; counting sign of number b
					call get_sign
					mov qword [signb], rax			; assigning sign of b to signb

countgractiona:		push qword [a]					; counting fraction of number a
					call get_significant
					mov qword [significanta], rax	; assigning fraction of a to significanta	
countfractionb:		push qword [b]					; counting fraction of number b
					call get_significant
					mov qword [significantb], rax 	; assigning fraction of b to significantb

countexpa:			push qword [a]					; counting exponent of number a
					call get_exp
					mov qword [expa], rax			; assigning exponent of a to expa
countexpb:			push qword [b]					; counting exponent of number b
					call get_exp
					mov qword [expb], rax			; assigning exponent of b to expb

checka0:			cmp qword [expa], 0				; checking if a is zero - exponent = 0, omitting base
					jne checkb0						; jump to checking if b is zero when expa != 0
					mov rax, qword[b]				; a is zero so second value is a result
					jmp leavep						; jump to the end of the function

checkb0:			cmp qword [expb], 0				; checking if b is zero - exponent = 0, omitting base
					jne checkainf					; jump to checking if a is +/-inf when expb != 0
					mov rax, qword[a]				; b is zero so first value is a result
					jmp leavep						; jump to the end of function

checkainf:			cmp qword [expa], 2047			; checking if a is +/- inf - expa = 2047, omitting base
					jne checkbinf					; jump to checking if b is +/-inf when expa != 2047
					mov rax, qword [expa]			; comparing if b is also +/-inf
					mov rbx, qword [expb]		
					cmp rax, rbx
					jne returninf					; if b is not +/- then there is only one inf, so result will be +/-inf
					
checkingtwoinf:		mov rax, qword [signa]			; b is also +/-inf so comparing signs
					mov rbx, qword [signb]
					cmp rax, rbx
					je returninf					; if signs are the same result is +/-inf
					
returnnan:			mov rax, qword [expa]			; signs are different so result will be NaN
					mov qword [exp], rax			; in case of NaN exp = 2047, omitting base
					mov qword [significanta], 1 	; fraction is != 0
					jmp ret2						; jump to create NaN

returninf:			mov rax, qword [a]				; result is +/-inf, so there is one inf or two have the same sign
					jmp leavep 						; jump to the end of function

checkbinf:			cmp qword [expb], 2047			; checking if b is +/- inf - expb = 2047, omitting base
					jne compexp						; if expb != 2047 then there are two normal number so jumping to compering exponents
					mov rax, qword[b]				; b is +/-inf and this is the only inf, so it will be a result
					jmp leavep						; jump to the end of function

compexp:			mov rdx, qword [expb]			; comparing two expenents to get the greater one and adjust fractions
					mov rcx, qword [expa]
					cmp rcx, rdx
					je expeq						; exponents are the same
					jg expgt						; exponent of a is greater
					jl explt						; exponent of b is greater

expeq:				mov rcx, qword [expa]			; if two exponents are the same is nothing to adjust
					mov qword [exp], rcx			; setting exp of result to expa
					jmp compsign					; jump to comparing signs of numbers

expgt:				mov rcx, qword [expa]			; exponent of a is greater so there is a need of adjustment
					mov qword [exp], rcx			; setting exp of result to expa, which is greater
					sub qword [expb], rcx			; adjusting fraction of b, by shifting it to right by expa-expb positions

shiftb:				cmp qword[expb], 0				; checking if fraction of b is fully adjusted
					je compsign						; if yes then jumping to comparing signs of numbers
					shr qword [significantb], 1 	; there is still need of adjustment so shifting fraction of b by 1
					add qword [expb], 1 			; and incrementing expb by 1
					jmp shiftb  					; jumping to the beginning of the loop

explt:				mov rdx, qword [expb]			; exponent of b is greater so there is a need of adjustment
					mov qword [exp], rdx			; setting exp of result to expb, which is greater
					sub qword [expa], rdx			; adjusting fraction of a, by shifting it to right by expb-expa positions

shifta:				cmp qword [expa], 0				; checking if fraction of a is fully adjusted
					je compsign						; if yes then jumping to comparing signs of numbers
					shr qword [significanta], 1 	; there is still need of adjustment so shifting fraction of a by 1
					add qword[expa], 1 				; and incrementing expa by 1
					jmp shifta 						; jumping to the beginning of the loop

compsign:			mov rdx, qword [signb]			; comparing two signs to determin if it is addition or substraction
					mov rcx, qword [signa]
					cmp rcx, rdx
					jne diffs						; there are different signs so act as substraction

sames:				mov rax, qword [significantb]	; there are same signs so act as normal addition
					add qword [significanta], rax
					jmp normalize 					; jumping to normalizing number

diffs:				mov rax, qword [significantb] 	; acting as substraction
					sub qword [significanta], rax

normalize:			mov rax, 1 						; checking if fraction is greater than 1.0000....
					shl rax, LEN_SIG_EX
					cmp qword [significanta], rax
					jl  normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg  normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je rets							; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], 0 				; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					mov qword [significanta], 0 	; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp ret2 						; jumping to create result

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, LEN_SIG_EX
					mov rdx, rcx
					and rcx, qword [significanta]
					cmp rcx, rdx
					je rets 						; fraction is normalized so jumping to create result

					sub qword [exp], 1  			; normalizing by one position, so decreasing exp
					shl qword [significanta], 1 	; shifting factor to left 
					jmp normalizel 					; jumping to beginning of the loop

normalizer:			cmp qword [exp], 2047			; checking if exp is 2047 - max value of exponent
					jne increaseexp 				; if not then continue computation 				
					mov qword [significanta], 0 	; exp is 2047 so result is inf, overflow occured. Setting fraction of result to 0 to express signed infinity.
					jmp ret2 						; jumping to create result

increaseexp:		mov rcx, qword [significanta] 	; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, LEN_SIG_EX 
					cmp rcx, 1
					je rets 						; fraction is normalized so jumping to create result

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [significanta], 1 	; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

rets:				shr qword [significanta], LEN_SIG_EXT 	; use only 52 meaningful bits
					push qword [significanta] 		; removing 1 from fraction so only part to right from . is kept
					call prepare_significant 		
					mov qword [significanta], rax

ret2:				mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EX
					add rax, qword [exp]
					shl rax, LEN_SIG
					add rax, qword [significanta]

leavep:				leave 							; leaving function
					ret
