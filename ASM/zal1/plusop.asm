; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 1 - Double Precision Floating Point Arythmetic
; File: plusop.asm - Implementacja dodawania

section .bss
    	a:   			resq    1
    	b:	 			resq	1
    	fractiona:		resq	1
    	fractionb:		resq	1
    	exp:			resq	1
    	signa: 			resq	1
    	signb: 			resq	1
    	expa: 			resq	1
    	expb: 			resq	1

section .text
        			global plus
        			extern get_sign, get_exp, get_fraction, prepare_fraction, LEN_EXPONENT, LEN_FRACTION, EXT_LEN_FRACTION, MAX_EXP, MIN_EXP
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
					call get_fraction
					mov qword [fractiona], rax		; assigning fraction of a to fractiona
					shl qword [fractiona], 1		; using Guard bit 
countfractionb:		push qword [b]					; counting fraction of number b
					call get_fraction
					mov qword [fractionb], rax 		; assigning fraction of b to fractionb
					shl qword [fractionb], 1		; using Guard bit 

countexpa:			push qword [a]					; counting exponent of number a
					call get_exp
					mov qword [expa], rax			; assigning exponent of a to expa
countexpb:			push qword [b]					; counting exponent of number b
					call get_exp
					mov qword [expb], rax			; assigning exponent of b to expb

checka0:			cmp qword [expa], MIN_EXP 		; checking if a is zero - exponent = 0, unbiased format
					jne checkb0						; jump to checking if b is zero when expa != 0
					mov rax, qword[b]				; a is zero so second value is a result
					jmp leavep						; jump to the end of the function

checkb0:			cmp qword [expb], MIN_EXP		; checking if b is zero - exponent = 0, unbiased format
					jne checkainf					; jump to checking if a is +/-inf when expb != 0
					mov rax, qword[a]				; b is zero so first value is a result
					jmp leavep						; jump to the end of function

checkainf:			cmp qword [expa], MAX_EXP		; checking if a is +/- inf - expa = 2047, unbiased format
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
					mov qword [exp], rax			; in case of NaN exp = 2047, unbiased format
					mov qword [fractiona], 1 		; fraction is != 0
					jmp createresult				; jump to NaN creation

returninf:			mov rax, qword [a]				; result is +/-inf, so there is one inf or two have the same sign
					jmp leavep 						; jump to the end of function

checkbinf:			cmp qword [expb], MAX_EXP		; checking if b is +/- inf - expb = 2047, omitting base
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

shiftb:				cmp qword[expb], MIN_EXP		; checking if fraction of b is fully adjusted
					je compsign						; if yes then jumping to comparing signs of numbers
					shr qword [fractionb], 1 		; there is still need of adjustment so shifting fraction of b by 1
					add qword [expb], 1 			; and incrementing expb by 1
					jmp shiftb  					; jumping to the beginning of the loop

explt:				mov rdx, qword [expb]			; exponent of b is greater so there is a need of adjustment
					mov qword [exp], rdx			; setting exp of result to expb, which is greater
					sub qword [expa], rdx			; adjusting fraction of a, by shifting it to right by expb-expa positions

shifta:				cmp qword [expa], MIN_EXP		; checking if fraction of a is fully adjusted
					je compsign						; if yes then jumping to comparing signs of numbers
					shr qword [fractiona], 1 		; there is still need of adjustment so shifting fraction of a by 1
					add qword[expa], 1 				; and incrementing expa by 1
					jmp shifta 						; jumping to the beginning of the loop

compsign:			mov rdx, qword [signb]			; comparing two signs to determin if it is addition or substraction
					mov rcx, qword [signa]
					cmp rcx, rdx
					jne diffs						; there are different signs so act as substraction

sames:				mov rax, qword [fractionb]		; there are same signs so act as normal addition
					add qword [fractiona], rax
					jmp normalize 					; jumping to normalizing number

diffs:				mov rax, qword [fractionb] 		; acting as substraction
					sub qword [fractiona], rax

normalize:			mov rax, 1 						; checking if fraction is greater than 1.0000....
					shl rax, EXT_LEN_FRACTION		; Guard bit is used so fraction is 53 bits long
					cmp qword [fractiona], rax
					jl  normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg  normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je adjustfraction				; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], MIN_EXP 		; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					mov qword [fractiona], 0 		; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp createresult 				; jumping to result creation

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, EXT_LEN_FRACTION
					mov rdx, rcx
					and rcx, qword [fractiona]
					cmp rcx, rdx
					je adjustfraction 				; fraction is normalized so jumping to adjusting a fraction

					sub qword [exp], 1  			; normalizing by one position, so decreasing exp
					shl qword [fractiona], 1 		; shifting factor to left 
					jmp normalizel 					; jumping to beginning of the loop

normalizer:			cmp qword [exp], MAX_EXP		; checking if exp is 2047 - max value of exponent
					jne increaseexp 				; if not then continue computation 				
					mov qword [fractiona], 0 		; exp is 2047 so result is inf, overflow occured. Setting fraction of result to 0 to express signed infinity.
					jmp createresult 				; jumping to result creation

increaseexp:		mov rcx, qword [fractiona] 		; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, EXT_LEN_FRACTION 
					cmp rcx, 1
					je adjustfraction 				; fraction is normalized so jumping to adjusting a fraction

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [fractiona], 1 		; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

adjustfraction:		shr qword [fractiona], 1 		; used guard bit, so now collect only 52 most eaningful bits
					push qword [fractiona] 			; removing 1 from fraction so only part to right from . is kept
					call prepare_fraction 		
					mov qword [fractiona], rax

createresult:		mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EXPONENT
					add rax, qword [exp]
					shl rax, LEN_FRACTION
					add rax, qword [fractiona]

leavep:				leave 							; leaving function
					ret
