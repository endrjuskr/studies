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

	mov ebx, dword [addr_a]
	movaps xmm0, [ebx]

	mov ecx, 0

	mov eax, dword [addr_b]
	add ecx, eax
	mov ebx, [ecx]
	mov [tmp], ebx

	mov eax, dword [size]
	shl eax, 2
	add ecx, eax
	mov eax, dword [addr_b]
	mov ebx, [ecx]
	mov [tmp + 4], ebx
	
	mov eax, dword [size]
	shl eax, 2
	add ecx, eax
	mov eax, dword [addr_b]
	mov ebx, [ecx]
	mov [tmp + 8], ebx
	
	mov eax, dword [size]
	shl eax, 2
	add ecx, eax
	mov eax, dword [addr_b]
	mov ebx, [ecx]
	mov [tmp + 12], ebx


	movups xmm1, [tmp]
	mulps  xmm0, xmm1

	haddps xmm0, xmm0
	haddps xmm0, xmm0

	movss dword [wynik], xmm0
	mov eax, dword [wynik]
	leave
	ret