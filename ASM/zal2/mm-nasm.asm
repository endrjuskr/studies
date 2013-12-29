; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 2 - Optymalizacja "rownolegla"
; File: mm-nasm.asm - mnozenie macierzy 

section .bss
	size:	resq 1
	matrix_c: resq 1
	esize: resq 1
	addr_a: resq 1
	addr_b: resq 1
	addr_c: resq 1
	cur_addr_a: resq 1
	cur_addr_b: resq 1
	cur_addr_c: resq 1
	counter: resq 1

section .text
	global optimal_mm

optimal_mm:
	enter 0,0
read_size:
	mov qword [size], rax ; matrix size
calculate_matrix_count:
	shr rax, 2
	mov qword [matrix_c], rax
calculate_row_size:
	shl rax, 4
	mov qword [esize], rax
read_b_addr:
	mov qword [addr_b], rsi ; drugi argument
read_a_addr:
	mov qword [addr_a], rdx ; trzeci argument
read_c_addr:
	mov qword [addr_c], rcx  ; czwarty argument

	mov rcx, 0 					; rcx indicates which 4x4 matrix we are calculating
for:
	mov rax, qword [matrix_c]
	imul rax, qword [matrix_c]
	cmp rcx, rax
	je end 						; after filling whole matrix (size * size) jump to end

calculate_current_matrix:
	mov rax, rcx
	mov rdx, 0
	mov rbx, qword [matrix_c]
	div rbx						; eax determines which row, edx which column

	mov rbx, qword [addr_b]
	shl rax, 2
	imul rax, qword [esize]
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

	mov rdi, 0
for_col:
	cmp rdi, qword [esize]
	je end_col


	mov qword [counter], 0
for_small:
	cmp qword [counter], 16
	je check_col
	
	mov rbx, rdi
	imul rbx, qword [size]
	add rbx, qword [counter]
	add rbx, qword [cur_addr_a]

	mov eax, dword [rbx]
	push rax
	add rbx, qword [esize]
	mov eax, dword [rbx]
	push rax
	add rbx, qword [esize]
	mov eax, dword [rbx]
	push rax
	add rbx, qword [esize]
	mov eax, dword [rbx]
	push rax

	movups xmm0, [rsp]
	movups xmm1, [rsp+16]
	haddps xmm0, xmm0
	haddps xmm1, xmm1
	movlhps xmm0, xmm1
	
	shufps xmm0, xmm0, 1Bh
	
	mov rbx, qword [cur_addr_b]
	add rbx, rdi

	movaps xmm1, [rbx]
	add rbx, qword [esize]
	movaps xmm2, [rbx]
	add rbx, qword [esize]
	movaps xmm3, [rbx]
	add rbx, qword [esize]
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

	add rax, qword [esize]

	movss xmm5, [rax]
	addss xmm2, xmm5
	movss [rax], xmm2

	add rax, qword [esize]

	movss xmm5, [rax]
	addss xmm3, xmm5
	movss [rax], xmm3

	add rax, qword [esize]

	movss xmm5, [rax]
	addss xmm4, xmm5
	movss [rax], xmm4

	add qword [counter], 4
	jmp for_small

check_col:
	add rdi, 16
	jmp for_col

end_col:
	add rcx, 1
	jmp for
end:
	leave
	ret