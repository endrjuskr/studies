section .text
		global minus
		extern plus
minus:
		enter 0, 0
		mov rcx, 1
		shl rcx, 63
		xor rbx, rcx
		call plus
		leave
		ret