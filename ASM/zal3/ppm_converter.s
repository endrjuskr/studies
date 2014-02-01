@Andrzej Skrodzki 292510
.text
.global convert_ppm

.set ENABLE_STURATION, 1

convert_ppm:                @ r0 - adres, r1 - width, r2 - height, r3 - ktory komponent, r4 - o ile zmiana
    push {r4-r8,lr}         @ musimy zachowac owe rejestry
    mul r5, r1, r2          @ wielkosc calej matrycy czyli width * height
    mov r6, #0              @ counter
    ldr r4, [sp, #24]       @ r4 jest na stosie
loop:
    cmp r6, r5              @ koniec? 
    beq end                 @ przeszlismy cala tablice
count_pixel:
    mov r7, r6
    add r7, r7, r7, LSL #1  @ wyznaczamy pixel  - * 3
count_component:
    add r7, r7, r3          @ wyznaczamy, ktory komponent
    add r7, r7, r7
    add r7, r7, r7
    ldr r8, [r0, r7]        @ znajdujemy to w tablicy
convertion:
    add r8, r8, r4
.ifdef ENABLE_STURATION
    cmp r8, #255           @ sprawdzamy czy nie wyszlo poza zakres gorny
    movgt r8, #255
    cmp r8, #0             @ sprawdzamy czy nie wyszlo poza zakres dolny
    movlt r8, #0
.endif
    str r8, [r0, r7]       @ zapisujemy to do tablicy
inc_loop:
    add r6, r6, #1
    b loop
end:
    pop {r4-r8,lr}         @ przywracamy wymagane rejestry
    bx lr
    