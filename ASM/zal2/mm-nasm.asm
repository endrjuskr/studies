; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 2 - Optymalizacja "rownolegla"
; File: mm-nasm.asm - mnozenie macierzy 

section .bss
	size:	resq 1 					; indicates size of matrix
	matrix_c: resq 1 				; indicates number of small matrix in a row
	msize: resq 1 					; indicates size of one row in memory
	addr_a: resq 1
	addr_b: resq 1
	addr_c: resq 1
	cur_addr_a: resq 1 				; indicates where is first cell of current small matrix of A
	cur_addr_b: resq 1 				; indicates where is first cell of current small matrix of B
	cur_addr_c: resq 1 				; indicates where is first cell of current small matrix of C
	counter: resq 1                 ; indicates which column in small matrix is on stack

section .text
	global naive_mm

naive_mm:
	enter 0,0
read_size:
	mov qword [size], rax
calculate_matrix_count:
	shr rax, 2
	mov qword [matrix_c], rax
calculate_row_size:
	shl rax, 4
	mov qword [msize], rax
read_b_addr:
	mov qword [addr_b], rsi 		; second argument
read_a_addr:
	mov qword [addr_a], rdx 		; third argument
read_c_addr:
	mov qword [addr_c], rcx  		; fourth argument

clear_c:
	mov rcx, 0
	mov rax, qword [size]
	imul rax, qword [msize]
loop_clear_c:
	cmp rax, rcx
	je matrix_multiplication
	mov rbx, qword[addr_c]
	add rbx, rcx
	add rcx, 4
	mov [rbx], dword 0
	jmp loop_clear_c
matrix_multiplication:
	mov rcx, 0 					; rcx indicates which 4x4 matrix we are calculating now
loop_m:
	mov rax, qword [matrix_c]
	imul rax, qword [matrix_c]
	cmp rcx, rax
	je end 						; after filling whole matrix (size * size) jump to end

calculate_current_matrix:
	mov rax, rcx
	mov rdx, 0
	mov rbx, qword [matrix_c]
	div rbx						; rax determines which row, rdx which column

	mov rbx, qword [addr_b]
	shl rax, 2
	imul rax, qword [msize]
	add rbx, rax
	mov qword [cur_addr_b], rbx

	mov rbx, qword [addr_a]
	shl rdx, 4
	add rbx, rdx
	mov qword [cur_addr_a], rbx

	mov rbx, qword [addr_c]
	add rbx, rax
	add rbx, rdx
	mov qword [cur_addr_c], rbx

	mov rdi, 0					; rdi indicates shift
loop_row:
	cmp rdi, qword [msize]
	je go_next_m


	mov qword [counter], 0
multiply_m:
	cmp qword [counter], 16
	je check_shift
	
	mov rbx, rdi
	imul rbx, qword [size]
	add rbx, qword [counter]
	add rbx, qword [cur_addr_a]

	mov eax, dword [rbx]    ;use stack to get column
	push rax
	add rbx, qword [msize]
	mov eax, dword [rbx]
	push rax
	add rbx, qword [msize]
	mov eax, dword [rbx]
	push rax
	add rbx, qword [msize]
	mov eax, dword [rbx]
	push rax

	movups xmm0, [rsp]
	movups xmm1, [rsp+16]
	add rsp, 32
	haddps xmm0, xmm0
	haddps xmm1, xmm1
	movlhps xmm0, xmm1
	
	shufps xmm0, xmm0, 1Bh
	
	mov rbx, qword [cur_addr_b]
	add rbx, rdi

	movaps xmm1, [rbx]
	add rbx, qword [msize]
	movaps xmm2, [rbx]
	add rbx, qword [msize]
	movaps xmm3, [rbx]
	add rbx, qword [msize]
	movaps xmm4, [rbx]

	movaps xmm6, xmm1
	movups xmm7, xmm0

	mulps  xmm1, xmm0
	mulps  xmm2, xmm0
	mulps  xmm3, xmm0
	mulps  xmm4, xmm0

	haddps xmm1, xmm1
	haddps xmm1, xmm1

	haddps xmm2, xmm2
	haddps xmm2, xmm2

	haddps xmm3, xmm3
	haddps xmm3, xmm3

	haddps xmm4, xmm4
	haddps xmm4, xmm4

	mov rax, qword [cur_addr_c]
	add rax, qword [counter]

	movss xmm5, [rax]
	addss xmm1, xmm5
	movss [rax], xmm1

	add rax, qword [msize]

	movss xmm5, [rax]
	addss xmm2, xmm5
	movss [rax], xmm2

	add rax, qword [msize]

	movss xmm5, [rax]
	addss xmm3, xmm5
	movss [rax], xmm3

	add rax, qword [msize]

	movss xmm5, [rax]
	addss xmm4, xmm5
	movss [rax], xmm4

	add qword [counter], 4
	jmp multiply_m

check_shift:
	add rdi, 16
	jmp loop_row

go_next_m:
	add rcx, 1
	jmp loop_m
end:
	leave
	ret