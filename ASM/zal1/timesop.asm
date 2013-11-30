; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 1 - Double Precision Floating Point Arythmetic
; File: times.asm - Implementacja mnozenia

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
        			global $times
        			extern get_sign, get_exp, get_fraction, prepare_fraction, LEN_EXPONENT, LEN_FRACTION, EXT_LEN_FRACTION, MAX_EXP, MIN_EXP, BASE

$times:				enter 0, 0
assigna:			mov qword [a], rax				; assigning first number to a
assignb:			mov qword [b], rbx  			; assigning second number to b

countsigna:			push qword [a]					; counting sign of number a
					call get_sign
					mov qword [signa], rax			; assigning sign of a to signa
					add rsp, 8						; clear stack	
countsignb:			push qword [b]					; counting sign of number b
					call get_sign
					mov qword [signb], rax			; assigning sign of b to signb
					add rsp, 8						; clear stack	

countgractiona:		push qword [a]					; counting fraction of number a
					call get_fraction
					mov qword [fractiona], rax		; assigning fraction of a to fractiona
					add rsp, 8						; clear stack	
countfractionb:		push qword [b]					; counting fraction of number b
					call get_fraction
					mov qword [fractionb], rax 		; assigning fraction of b to fractionb
					add rsp, 8						; clear stack

countexpa:			push qword [a]					; counting exponent of number a
					call get_exp
					mov qword [expa], rax			; assigning exponent of a to expa
					sub qword [expa], BASE			; substrack base
					add rsp, 8						; clear stack
countexpb:			push qword [b]					; counting exponent of number b
					call get_exp
					mov qword [expb], rax			; assigning exponent of b to expb
					sub qword [expb], BASE			; substrack base
					add rsp, 8						; clear stack

checka0:			cmp qword [expa], -1023 		; checking if a is zero - exponent = -1023, biased format
					jne checkb0						; jump to checking if b is zero when expa != -1023
					mov rcx, qword [signb]			; if a is zero let's check sign
					shl rcx, 63
					xor rcx, qword [a]				; xor will result with correct sign
					mov rax, rcx					
					jmp leavep						; jump to the end of the function

checkb0:			cmp qword [expb], -1023 		; checking if b is zero - exponent = -1023, biased format
					jne checkainf					; jump to checking if a is +/-inf when expb != -1023
					mov rcx, qword [signa]			; if b is zero let's check sign
					shl rcx, 63
					xor rcx, qword [b]				; xor will result with correct sign
					mov rax, rcx										
					jmp leavep						; jump to the end of function

checkainf:			cmp qword [expa], 1024 			; checking if a is +/- inf - expa = 1024, biased format
					jne checkbinf					; jump to checking if b is +/-inf when expa != 1024
					mov rcx, qword [signb]			; if a is +/-inf let's check sign
					shl rcx, 63
					xor rcx, qword [a]				; xor will result with correct sign
					mov rax, rcx					
					jmp leavep 						; jump to the end of function

checkbinf:			cmp qword [expb], 1024 			; checking if b is +/- inf - expb = 1024, biased format
					jne calculateexp						; if expb != 1024 then there are two normal number so jumping to compering exponents
					mov rcx, qword [signa]			; if b is +/-inf let's check sign
					shl rcx, 63
					xor rcx, qword [b]				; xor will result with correct sign
					mov rax, rcx					
					jmp leavep						; jump to the end of function

calculateexp:		mov rax, qword [expa]			; adding two exponents 
					mov qword [exp], rax
					mov rax, qword [expb]
					add qword [exp], rax
					add qword [exp], BASE			; add base, becase there will be only normalization in the future

comperingexp:		cmp qword [exp], MAX_EXP 		; comapring exponent. Only possible option is overflow, becasue exponents are added
					jl normalize
					mov qword [exp], MAX_EXP
					mov qword [fractiona], 0
					jmp calculatesign

normalize:			mov rax, qword [fractiona]		; multiplying two fractions
					mov rbx, qword [fractionb]
					mul rbx							; result is stored like this rdx:rax
					shl rdx, 12 					; result should be 54 the most significant bits. 54 becase it is before normalization. Taking 42 bits from rdx.
					shr rax, 52						; taking 12 bits from rax. here bits are less signicant
					mov qword [fractiona], rdx		; creating 54 bits fraction
					add qword [fractiona], rax

					mov rax, 1 						; checking if fraction is greater than 1.0000....
					shl rax, LEN_FRACTION
					cmp qword [fractiona], rax
					jl normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je adjustfraction							; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], MIN_EXP	; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					mov qword [fractiona], 0 		; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp createresult 				; jumping to create result

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, LEN_FRACTION
					mov rdx, rcx
					and rcx, qword [fractiona]
					cmp rcx, rdx
					je adjustfraction 				; fraction is normalized so jumping to create result

					sub qword [exp], 1  			; normalizing by one position, so decreasing exp
					shl qword [fractiona], 1 		; shifting factor to left 
					jmp normalizel 					; jumping to beginning of the loop

normalizer:			cmp qword [exp], MAX_EXP	; checking if exp is 2047 - max value of exponent
					jne increaseexp 				; if not then continue computation 				
					mov qword [fractiona], 0 		; exp is 2047 so result is inf, overflow occured. Setting fraction of result to 0 to express signed infinity.
					jmp createresult 				; jumping to create result

increaseexp:		mov rcx, qword [fractiona] 		; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, LEN_FRACTION 
					cmp rcx, 1
					je adjustfraction 				; fraction is normalized so jumping to create result

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [fractiona], 1 		; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

adjustfraction:		push qword [fractiona] 			; removing 1 from fraction so only part to right from . is kept
					call prepare_fraction 		
					mov qword [fractiona], rax
					add rsp, 8						; clear stack

calculatesign:		mov rax, qword [signb]			; calculating sign
					xor qword [signa], rax

createresult:		mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EXPONENT
					add rax, qword [exp]
					shl rax, LEN_FRACTION
					add rax, qword [fractiona]

leavep:				leave 							; leaving function
					ret
