; multi–segment executable file template.
data segment
    NAME1 DB 'ABCDEFGHI'
    NAME2 DB 'JKLMNOPQR'
    NAME3 DB 'STUVWXYZ*'
ends

stack segment
    dw 128 dup(0)
ends

code segment
start:
    ; set segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax
    
    ; add your code here
    LEA SI, NAME1   ; Инициализация адресов
    LEA DI, NAME2   ; NAME1 и NAME2
    MOV CX, 09      ; Переслать 9 символов
    REP MOVSB
    
    LEA SI, NAME2   ; Инициализация адресов
    LEA DI, NAME3   ; NAME2 и NAME3
    MOV CX, 09      ; переслать 9 символов
    REP MOVSB
                    
    mov ax, 4c00h   ; exit to operating system.
    int 21h
ends

end start ; set entry point and stop the assembler.
