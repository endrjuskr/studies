section .text
		global minus
		extern plus
minus:
		enter 0, 0
		imul rbx, -1
		call plus
		leave
		ret