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
        			extern get_sign, get_exp, get_fraction, prepare_fraction, LEN_EX, LEN_SIG, LEN_SIG_EX, LEN_SIG_EXT

divide:				enter 0, 0
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
					shr qword [fractiona], 1
countfractionb:		push qword [b]					; counting fraction of number b
					call get_fraction
					mov qword [fractionb], rax 		; assigning fraction of b to fractionb
					shr qword [fractionb], 1

countexpa:			push qword [a]					; counting exponent of number a
					call get_exp
					mov qword [expa], rax			; assigning exponent of a to expa
					sub qword [expa], 1023
countexpb:			push qword [b]					; counting exponent of number b
					call get_exp
					mov qword [expb], rax			; assigning exponent of b to expb
					sub qword [expb], 1023

checkb0:			cmp qword [expb], -1023			; checking if b is zero - exponent = 0, omitting base
					jne checka0					; jump to checking if a is +/-inf when expb != 0
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], 2047
					mov qword [fractiona], 0
					jmp ret2						; jump to create result

checka0:			cmp qword [expa], -1023			; checking if b is zero - exponent = 0, omitting base
					jne checkbinf					; jump to checking if a is +/-inf when expb != 0
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], 0
					mov qword [fractiona], 0
					jmp ret2						; jump to create result

checkbinf:			cmp qword [expb], 1024			; checking if b is +/- inf - expb = 2047, omitting base
					jne checkainf						; if expb != 2047 then there are two normal number so jumping to compering exponents
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], 0
					mov qword [fractiona], 0
					jmp ret2						; jump to create result

checkainf:			cmp qword [expa], 1024			; checking if b is +/- inf - expb = 2047, omitting base
					jne calculateexp						; if expb != 2047 then there are two normal number so jumping to compering exponents
					mov rax, qword [signb]
					xor qword [signa], rax
					mov qword [exp], 2047
					mov qword [fractiona], 0
					jmp ret2						; jump to create result

calculateexp:		mov rax, qword [expa]			; comparing two expenents to get the greater one and adjust fractions
					mov qword [exp], rax
					mov rax, qword [expb]
					sub qword [exp], rax
					add qword [exp], 1023
					mov rax, 1
					shl rax, LEN_EX
					sub rax, 1
					cmp qword [exp], rax
					jl checkexp0
					mov qword [exp], 1
					shl qword [exp], LEN_EX
					sub qword [exp], 1
					mov qword [fractiona], 0
					jmp calculatesign
checkexp0:			cmp qword [exp], 0
					jg normalize
					mov qword [exp], 0
					mov qword [fractiona], 0
					jmp calculatesign
normalize:			mov rcx, 53
					mov rax, qword [fractiona]
					mov qword [fractiona], 0
					mov qword [remain], rax
divisionloop: 		cmp rcx, 0
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
					shl rax, LEN_SIG_EX
					cmp qword [fractiona], rax
					jl normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je rets							; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], 0 				; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					;mov qword [fractiona], 0 		; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp calculatesign 						; jumping to create result

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, LEN_SIG_EX
					mov rdx, rcx
					and rcx, qword [fractiona]
					cmp rcx, rdx
					je rets 						; fraction is normalized so jumping to create result

					sub qword [exp], 1  			; normalizing by one position, so decreasing exp
					shl qword [fractiona], 1 		; shifting factor to left 
					jmp normalizel 					; jumping to beginning of the loop

normalizer:			cmp qword [exp], 2047			; checking if exp is 2047 - max value of exponent
					jne increaseexp 				; if not then continue computation 				
					mov qword [fractiona], 0 		; exp is 2047 so result is inf, overflow occured. Setting fraction of result to 0 to express signed infinity.
					jmp calculatesign 						; jumping to create result

increaseexp:		mov rcx, qword [fractiona] 		; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, LEN_SIG_EX 
					cmp rcx, 1
					je rets 						; fraction is normalized so jumping to create result

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [fractiona], 1 		; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

rets:				shr qword [fractiona], LEN_SIG_EXT
					push qword [fractiona] 			; removing 1 from fraction so only part to right from . is kept
					call prepare_fraction 		
					mov qword [fractiona], rax
calculatesign:		mov rax, qword [signb]			; calculating sign
					xor qword [signa], rax

ret2:				mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EX
					add rax, qword [exp]
					shl rax, LEN_SIG
					add rax, qword [fractiona]

leavep:				leave 							; leaving function
					ret