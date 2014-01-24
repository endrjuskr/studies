@Andrzej Skrodzki 292510
.text
.global convert_ppm

convert_ppm:                @ r0 - adres, r1 - width, r2 - height, r3 - ktory komponent, r4 - o ile zmiana
    mov r5, r1              @ wielkosc calej matrycy czyli width * height
    mul r5, r5, r2
    mov r6, #0              @ counter
loop:
    cmp r6, r5              @ koniec? 
    beq end                 @ przeszlismy cala tablice
    mov r7, r6
    add r7, r7, r7, LSL #1  @ wyznaczamy pixel  - * 3
    add r7, r7, r3          @ wyznaczamy, ktory komponent
    ldr r8, [r0, r7]       @ znajdujemy to w tablicy
.ifdef ENABLE_STURATION
    adc r8, r8, r4          @ dodajemy, TODO: dodaj kompilacje warunkowa
.else
    adc r8, r8, r4
.endif
    str r8, [r0, r7]       @ zapisujemy to do tablicy
    b loop
end:
    bx lr
-
