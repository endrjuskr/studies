; Andrzej Skrodzki 292510
; Programowanie w Asemblerze
; Zadanie zaliczeniowe 1 - Double Precision Floating Point Arythmetic
; File: numberpartition.asm - Implementacja pobierania poszczegolnych czesci liczby wedlug formatu IEEE

global get_fraction, get_exp, get_sign, prepare_fraction, LEN_FRACTION, LEN_EXPONENT, EXT_LEN_FRACTION, MAX_EXP, MIN_EXP, BASE

LEN_FRACTIONN  equ 1
LEN_EXPONENT    equ 11
LEN_FRACTION   equ 52
EXT_LEN_FRACTION equ 53
EXT_LEN_FRACTIONT equ 1
MAX_EXP equ 2047
MIN_EXP equ 0
BASE equ 1023

section .text
get_fraction:		; Gets significant from number which is represented by bits 52..0
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_FRACTION
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					mov rbx, 1
					shl rbx, LEN_FRACTION
					or  rax, rbx    	; Add 1 to number
					leave
					ret
get_exp:			; Gets exponent from number which is represented by bits 63..53 with added 1023
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					sal rbx, LEN_EXPONENT
					sub rbx, 1          ; get value 2^11 - 1
					shl rbx, LEN_FRACTION
					and rax, rbx 		; Collect bits 63..53
					shr rax, LEN_FRACTION
					leave
					ret
get_sign:			; Gets sign of number which is represented by bit 64
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					shr rax, LEN_EXPONENT + LEN_FRACTION
					leave
					ret
prepare_fraction:
					enter 0, 0
					mov rax, [rsp + 16] ; First argument
					mov rbx, 1
					shl rbx, LEN_FRACTION
					sub rbx, 1 			
					and rax, rbx 		; Collect only last 52 bits
					leave
					ret