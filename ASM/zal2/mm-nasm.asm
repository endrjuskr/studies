; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 2 - Optymalizacja "rownolegla"
; File: mm-nasm.asm - mnozenie macierzy 

section .bss
	size:	resd 1
	addr_a: resd 1
	addr_b: resd 1
	addr_c: resd 1
	wynik: 	resd 1
	wyn:	resd 1
	col_offset: resd 1
	counter: resd 1
	tmp:	resb 16

section .data
	value1: dd 0, 0, 0, 0

section .text
	global optimal_mm

optimal_mm:
	enter 0,0
	mov ebx, [esp + 8]
	mov dword [size], ebx ; matrix size

	mov ebx, [esp + 12]
	mov dword [addr_b], ebx ; drugi argument

	mov ebx, [esp + 16]
	mov dword [addr_a], ebx ; trzeci argument

	mov ebx, [esp + 20]
	mov dword [addr_c], ebx  ; czwarty argument

	mov dword [counter], 0
for:
	mov eax, dword [size]
	imul eax, dword [size]
	cmp eax, dword [counter]
	je end 						; after filling whole matrix (size * size) jump to end

clear_cell:
	mov eax, dword [addr_c]
	mov ecx, dword [addr_c]
	mov ebx, dword [counter]
	shl ebx, 2
	add eax, ebx

	mov ebx, 0
	mov [eax], ebx
	
	mov eax, dword [size]
	shl eax, 2
	mov dword [col_offset], eax

	movups xmm2, [value1]

add_vec:
	sub dword [col_offset], 16

	mov eax, dword [counter]
	mov edx, 0
	mov ebx, dword [size]
	div ebx						; eax determines which row, edx which column
	
	mov ebx, dword [addr_b]
	shl eax, 2
	imul eax, dword [size]
	add ebx, eax
	add ebx, dword [col_offset]
	movaps xmm0, [ebx]

	mov ebx, dword [addr_a]
	mov ecx, dword [col_offset]
	imul ecx, dword [size]
	add ebx, ecx
	imul edx, 4
	add ebx, edx
	mov eax, [ebx]
	mov [tmp], eax

	mov eax, dword [size]
	shl eax, 2
	add ebx, eax
	mov edx, [ebx]
	mov [tmp + 4], edx
	
	add ebx, eax
	mov edx, [ebx]
	mov [tmp + 8], edx
	
	add ebx, eax
	mov edx, [ebx]
	mov [tmp + 12], edx
	
	movups xmm1, [tmp]
	mulps  xmm0, xmm1
	addps  xmm2, xmm0

	mov eax, dword [col_offset]
	cmp eax, 0
	jne add_vec

	mov eax, dword [addr_c]
	mov ebx, dword [counter]
	shl ebx, 2
	add eax, ebx

	haddps xmm2, xmm2
	haddps xmm2, xmm2
	
	movss dword [wynik], xmm2
	mov ebx, dword [wynik]
	mov [eax], ebx

	add dword [counter], 1
	jmp for
end:
	leave
	ret