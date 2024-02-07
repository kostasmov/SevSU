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
    
    B20:
    MOV AL, [SI]    ; Переслать из NAME1
    MOV [DI], AL    ; Переслать в NAME2
    INC SI          ; Следующий символ вNAME1
    INC DI          ; Следующая позиция в NAME2
    DEC CX          ; Уменьшить счетчик цикла
    JNZ B20         ; Счетчик > 0? Да – цикл
    ; RET           ; Если счетчик = 0, то выйти из цикла
    
    LEA SI, NAME2   ; Инициализация адресов
    LEA DI, NAME3   ; NAME2 и NAME3
    MOV CX, 09      ; переслать 9 символов
    
    C20:
    MOV AL, [SI]    ; Переслать из NAME2
    MOV [DI], AL    ; Переслать в NAME3
    INC DI          ; следующий символ в NAME2
    INC SI          ; следующая позиция в NAME3
    LOOP C20        ; уменьшить счетчик,
                    ; если не ноль, то цикл
                    ; если счетчик 0, то вернуться
                    
    mov ax, 4c00h   ; exit to operating system.
    int 21h
ends

end start ; set entry point and stop the assembler.
