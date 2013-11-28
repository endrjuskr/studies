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
        			global times2
        			extern get_sign, get_exp, get_fraction, prepare_fraction, LEN_EX, LEN_SIG, LEN_SIG_EX, LEN_SIG_EXT
times2:				enter 0, 0
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

checka0:			cmp qword [expa], -1023				; checking if a is zero - exponent = 0, omitting base
					jne checkb0						; jump to checking if b is zero when expa != 0
					mov rcx, 1						; if a is zero let's check sign
					shl rcx, 63
					and rcx, qword [b]				; rcx has sign of b
					xor rcx, qword [a]				; xor will result with proper sign
					mov rax, rcx					
					jmp leavep						; jump to the end of the function

checkb0:			cmp qword [expb], -1023				; checking if b is zero - exponent = 0, omitting base
					jne checkainf					; jump to checking if a is +/-inf when expb != 0
					mov rcx, 1						; if b is zero let's check sign
					shl rcx, 63
					and rcx, qword [a]				; rcx has sign of a
					xor rcx, qword [b]				; xor will result with proper sign
					mov rax, rcx										
					jmp leavep						; jump to the end of function

checkainf:			cmp qword [expa], 1024			; checking if a is +/- inf - expa = 2047, omitting base
					jne checkbinf					; jump to checking if b is +/-inf when expa != 2047
					mov rcx, 1						; if a is inf let's check sign
					shl rcx, 63
					and rcx, qword [b]				; rcx has sign of b
					xor qword [a], rcx
					mov rax, qword [a]				; result is +/-inf, so there is one inf or two have the same sign
					jmp leavep 						; jump to the end of function

checkbinf:			cmp qword [expb], 1024			; checking if b is +/- inf - expb = 2047, omitting base
					jne calculateexp						; if expb != 2047 then there are two normal number so jumping to compering exponents
					mov rcx, 1						; if b is inf let's check sign
					shl rcx, 63
					and rcx, qword [a]				; rcx has sign of a
					xor qword [b], rcx
					mov rax, qword[b]				; b is +/-inf and this is the only inf, so it will be a result
					jmp leavep						; jump to the end of function

calculateexp:		mov rax, qword [expa]			; comparing two expenents to get the greater one and adjust fractions
					mov qword [exp], rax
					mov rax, qword [expb]
					add qword [exp], rax
					add qword [exp], 1023
					mov rax, 1
					shl rax, LEN_EX
					sub rax, 1
					cmp qword [exp], rax
					jl normalize
					mov qword [exp], 1
					shl qword [exp], LEN_EX
					sub qword [exp], 1
					mov qword [fractiona], 0
					mov rax, qword [signb]
					xor qword [signa], rax
					jmp ret2
normalize:			mov rax, qword [fractiona]		; multiplying two fractions
					mov rbx, qword [fractionb]
					mul rbx
					shl rdx, 12
					shr rax, 52
					mov qword [fractiona], rdx
					add qword [fractiona], rax
					mov rax, 1 						; checking if fraction is greater than 1.0000....
					shl rax, LEN_SIG
					cmp qword [fractiona], rax
					jl normalizel					; if fraction is less than 1.000... so there is a need of shifting fracion to left (increasing)
					jg normalizer					; if fraction is greater than 1.000... so there might be a need of shifting fracion to right (decreasing)
					je rets							; fraction is equal 1.000... so jumping to create result

normalizel:			cmp qword [exp], 0 				; checking if exp is 0 - min value of exponent
					jne decreaseexp 				; if not then continue computation
					mov qword [fractiona], 0 		; exp is 0 so result is 0, underflow occured. Setting fraction of result to 0 to express signed zero.
					jmp ret2 						; jumping to create result

decreaseexp:		mov rcx, 1 						; checking if there were enough shiftments - factor start with 1
					shl rcx, LEN_SIG
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
					jmp ret2 						; jumping to create result

increaseexp:		mov rcx, qword [fractiona] 		; checking if there were enough shiftments - factor start with 1. It might be greater than 1 
					shr rcx, LEN_SIG 
					cmp rcx, 1
					je rets 						; fraction is normalized so jumping to create result

					add qword [exp], 1 			 	; normalizing by one position, so increasing exp
					shr qword [fractiona], 1 		; shifting factor to right 
					jmp normalizer					; jumping to beginning of the loop

rets:				push qword [fractiona] 			; removing 1 from fraction so only part to right from . is kept
					call prepare_fraction 		
					mov qword [fractiona], rax
					mov rax, qword [signb]			; calculating sign
					xor qword [signa], rax

ret2:				mov rax, qword [signa] 			; preparing result by creating 64 number with proper sequence of double precision floating point number parts
					shl rax, LEN_EX
					add rax, qword [exp]
					shl rax, LEN_SIG
					add rax, qword [fractiona]

leavep:				leave 							; leaving function
					ret
