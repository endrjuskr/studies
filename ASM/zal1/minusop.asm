section .text
		global minus
		extern plus
minus:
		enter 0, 0			; substraction is addtion with opposite second number
		mov rcx, 1
		shl rcx, 63
		xor rbx, rcx  		; creating opposite number, by changing sign of number
		call plus 			; calling normal addition
		leave 				; result is in rax
		ret