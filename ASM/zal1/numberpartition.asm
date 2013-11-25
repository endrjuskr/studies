global get_significant, get_exp, get_sign, LEN_SIG, LEN_EX

LEN_SIGN  equ 1
LEN_EX    equ 11
LEN_SIG   equ 52

section .text
get_significant:	; Gets significant from number which is represented by bits 52..0
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_SIG
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					mov rbx, 1
					shl rbx, LEN_SIG
					or  rax, rbx    	; Add 1 to number
					leave
					ret
get_exp:			; Gets exponential from number which is represented by bits 63..53 with added 1023
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_EX
					sub rbx, 1          ; get value 2^11 - 1
					shr rbx, LEN_SIG
					and rax, rbx 		; Collect bits 63..53
					leave
					ret
get_sign:			; Gets sign of number which is represented by bit 64
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					shr rbx, LEN_EX + LEN_SIG
					leave
					ret