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
	tmp:	resb 16

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

	mov ecx, 0
for:
	mov eax, dword [size]
	imul eax, dword [size]
	cmp eax, ecx
	je end 						; after filling whole matrix (size * size) jump to end

clear_cell:
	mov eax, dword [addr_c]
	mov ebx, ecx
	imul ebx, 4
	add eax, ebx
	mov ebx, 0
	mov [eax], ebx

	mov eax, ecx
	mov edx, 0
	mov ebx, dword [size]
	div ebx				; eax determines which row, edx which column

	mov edi, dword [size]
	imul edi, 4

add_vec:
	sub edi, 16
	mov ebx, dword [addr_b]
	imul eax, 4
	imul eax, dword [size]
	add ebx, eax
	add ebx, edi
	movaps xmm0, [ebx]

	mov ebx, dword [addr_a]
	add ebx, edi
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

	haddps xmm0, xmm0
	haddps xmm0, xmm0

	mov eax, dword [addr_c]
	mov ebx, ecx
	imul ebx, 4
	add eax, ebx

	movss dword [wynik], xmm0
	mov ebx, dword [wynik]
	add [eax], ebx

	cmp edi, 0
	jne add_vec
	
	add ecx, 1
	jmp for
end:
	leave
	ret