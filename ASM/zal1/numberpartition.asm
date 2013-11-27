global get_fraction, get_exp, get_sign, prepare_fraction, LEN_SIG, LEN_EX, LEN_SIG_EX, LEN_SIG_EXT

LEN_SIGN  equ 1
LEN_EX    equ 11
LEN_SIG   equ 52
LEN_SIG_EX equ 53
LEN_SIG_EXT equ 1

section .text
get_fraction:		; Gets significant from number which is represented by bits 52..0
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_SIG
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					mov rbx, 1
					shl rbx, LEN_SIG
					or  rax, rbx    	; Add 1 to number
					shl rax, LEN_SIG_EXT   ; use all 64 bits
					leave
					ret
get_exp:			; Gets exponent from number which is represented by bits 63..53 with added 1023
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					sal rbx, LEN_EX
					sub rbx, 1          ; get value 2^11 - 1
					shl rbx, LEN_SIG
					and rax, rbx 		; Collect bits 63..53
					shr rax, LEN_SIG
					leave
					ret
get_sign:			; Gets sign of number which is represented by bit 64
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					shr rax, LEN_EX + LEN_SIG
					leave
					ret
prepare_fraction:
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_SIG
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					leave
					ret