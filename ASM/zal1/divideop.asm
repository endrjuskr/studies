; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 1 - Double Precision Floating Point Arythmetic
; File: divideop.asm - Implementacja dzielenia

section .bss
    	a:   			resq    1
    	b:	 			resq	1
    	fractiona:		resq	1
    	fractionb:		resq	1
    	remain			resq	1
    	exp:			resq	1
    	signa: 			resq	1
    	signb: 			resq	1
    	expa: 			resq	1
    	expb: 			resq	1

section .text
        			global divide
        			extern get_sign, get_exp, get_fraction, prepare_fraction, LEN_EXPONENT, LEN_FRACTION, EXT_LEN_FRACTION, MAX_EXP, MIN_EXP, BASE

divide:				enter 0, 0
assigna:			mov qword [a], rax						; assigning first number to a
assignb:			mov qword [b], rbx  					; assigning second number to b

countsigna:			push qword [a]							; counting sign of number a
					call get_sign
					mov qword [signa], rax					; assigning sign of a to signa
countsignb:			push qword [b]							; counting sign of number b
					call get_sign
					mov qword [signb], rax					; assigning sign of b to signb

countgractiona:		push qword [a]							; counting fraction of number a
					call get_fraction
					mov qword [fractiona], rax				; assigning fraction of a to fractiona	
countfractionb:		push qword [b]							; counting fraction of number b
					call get_fraction
					mov qword [fractionb], rax 				; assigning fraction of b to fractionb

countexpa:			push qword [a]							; counting exponent of number a
					call get_exp
					mov qword [expa], rax					; assigning exponent of a to expa
					sub qword [expa], BASE
countexpb:			push qword [b]							; counting exponent of number b
					call get_exp
					mov qword [expb], rax					; assigning exponent of b to expb
					sub qword [expb], BASE

checkb0:			cmp qword [expb], -1023					; checking if b is zero - exponent = -1023, biased format
					jne checka0								; jump to checking if a is +/-inf when expb != -1023
					cmp qword [expa], -1023					; checking if a is zero - exponent = -1023, biased format
					jne returninf			
					mov qword [exp], MAX_EXP
					mov qword [fractiona], 1
					jmp calculatesign				
returninf:			mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], MAX_EXP
					mov qword [fractiona], 0
					jmp createresult						; jump to create result

checka0:			cmp qword [expa], -1023					; checking if a is zero - exponent = -1023, biased format
					jne checkbinf							; jump to checking if b is +/-inf when expb != -1023
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], 0
					mov qword [fractiona], 0
					jmp createresult						; jump to create result

checkbinf:			cmp qword [expb], 1024					; checking if b is +/- inf - expb = 1024, biased format
					jne checkainf							; if expb != 1024 then there are two normal number so jumping to compering exponents
					cmp qword [expa], 1024					; check situation inf/inf, which results Nan
					jne oneinf
					mov qword [exp], MAX_EXP
					mov qword [fractiona], 1
					jmp calculatesign

oneinf:				mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], MIN_EXP
					mov qword [fractiona], 0
					jmp createresult						; jump to create result

checkainf:			cmp qword [expa], 1024					; checking if b is +/- inf - expb = 1024, biased format
					jne calculateexp						; if expb != 1024 then there are two normal number so jumping to compering exponents
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], MAX_EXP
					mov qword [fractiona], 0
					jmp createresult						; jump to create result

calculateexp:		mov rax, qword [expa]					; comparing two expenents to get the greater one and adjust fractions
					mov qword [exp], rax
					mov rax, qword [expb]
					sub qword [exp], rax
					add qword [exp], BASE
					mov rax, MAX_EXP
					cmp qword [exp], rax
					jl checkexp0

					mov qword [exp], MAX_EXP				; returning inf
					mov qword [fractiona], 0
					jmp calculatesign

checkexp0:			cmp qword [exp], MIN_EXP
					jg normalize
					mov qword [exp], MIN_EXP
					mov qword [fractiona], 0
					jmp calculatesign

normalize:			mov rcx, EXT_LEN_FRACTION
					mov rax, qword [fractiona]
					mov qword [fractiona], 0
					mov qword [remain], rax

divisionloop: 		cmp rcx, 0 								; performing division by getting full numbers and remain, like modulo. 
					je compareremain
					mov rdx, 0
					mov rax, qword [remain]
					mov rbx, qword [fractionb]
					div rbx
					shl qword [fractiona], 1
					add qword [fractiona], rax
					mov qword [remain], rdx
					shl qword [remain], 1
					sub rcx, 1
					jmp divisionloop

compareremain:		shl qword [fractiona], 1
					cmp qword [remain], 0
					je checkingfraction
					or qword [fractiona], 1

checkingfraction: 	mov rax, 1 						; checking if fraction is greater than 1.0000....
					shl rax, EXT_LEN_FRACTION
					cmp qword [fractiona], rax
					jl normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je adjustfraction				; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], MIN_EXP		; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					;mov qword [fractiona], 0 		; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp calculatesign 				; jumping to create result

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, EXT_LEN_FRACTION
					mov rdx, rcx
					and rcx, qword [fractiona]
					cmp rcx, rdx
					je adjustfraction 				; fraction is normalized so jumping to create result

					sub qword [exp], 1  			; normalizing by one position, so decreasing exp
					shl qword [fractiona], 1 		; shifting factor to left 
					jmp normalizel 					; jumping to beginning of the loop

normalizer:			cmp qword [exp], MAX_EXP		; checking if exp is 2047 - max value of exponent
					jne increaseexp 				; if not then continue computation 				
					mov qword [fractiona], 0 		; exp is 2047 so result is inf, overflow occured. Setting fraction of result to 0 to express signed infinity.
					jmp calculatesign 				; jumping to create result

increaseexp:		mov rcx, qword [fractiona] 		; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, EXT_LEN_FRACTION 
					cmp rcx, 1
					je adjustfraction 				; fraction is normalized so jumping to create result

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [fractiona], 1 		; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

adjustfraction:		shr qword [fractiona], 1
					push qword [fractiona] 			; removing 1 from fraction so only part to right from . is kept
					call prepare_fraction 		
					mov qword [fractiona], rax
calculatesign:		mov rax, qword [signb]			; calculating sign
					xor qword [signa], rax

createresult:		mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EXPONENT
					add rax, qword [exp]
					shl rax, LEN_FRACTION
					add rax, qword [fractiona]

leavep:				leave 							; leaving function
					ret
