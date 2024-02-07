; сегмент определения переменных
data segment
    v dw 12345
    pkey db 13, 10, 'Press any key...$'
ends

; сегмент стека
stack segment
    dw 128 dup(0)
ends
 
; сегмент исполняемого кода
code segment
start:
    mov ax, data        ; инициализация адресных регистров
    mov ds, ax          ;
    mov es, ax          ;

    mov bx, v           ; BX = v
    mov ah, 02h         ; код функции DOS 02h - вывод символа
    mov cx, 16          ; инициализация счётчика цикла
    
    lp:
    shl bx, 1           ; сдвиг BX на 1 бит влево
    mov dl, '0'         ; dl = '0'
    jnc print           ; переход, если выдвинутый бит равен 0
    inc dl              ; иначе dl = dl + 1 = '1'
    print:
    int 21h             ; вызов функции DOS 02h (вывод символа dl)
    loop lp             ; новая итерация цикла (пока cx != 0)
            
    lea dx, pkey        ; относительный адрес строки pkey
    mov ah, 09h         ; код функции DOS 09h - вывод строки
    int 21h             ; вывод строки 'Press any key...'
     
    mov ah, 01h         ; код функции DOS 01h - ожидание отклика
    int 21h             ; переход в режим ожидания
    
    mov ah, 4Ch         ; код функции DOS 4Ch - передача управления ОС
    int 21h             ; вызов функции DOS 4C, завершение программы
ends

end start
