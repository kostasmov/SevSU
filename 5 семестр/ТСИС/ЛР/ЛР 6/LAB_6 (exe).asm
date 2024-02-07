; Переменные
data segment
    x1 dw 10                        ; начальная координата x
    y1 dw 10                        ; начальная координата y
    x2 dw 0                         ; ширина прямоугольника
    y2 dw 0                         ; высота прямоугольника
    color db 10                     ; цвет линий
    enter_x db 'Введите ширину: $'  ;
    enter_y db 'Введите высоту: $'  ;
    enter_col db 'Введите цвет: $'  ;
    error db 'Некорректный ввод! $' ; сообщение об ошибке
    buff db 4, ?, 4 dup(?)          ; буфер для строки ввода
ends

; Сегмент стека
stack segment
    dw 128 dup(0)
ends

; Код программы
code segment
start:
    ; установка адресных регистров
    mov ax, data
    mov ds, ax
    mov es, ax
    mov cx, 0
    
    mov dx, offset enter_x  ; ввод ширины
    mov ah, 09h             ;
    int 21h                 ;
    call getInt             ; 
    mov x2, ax              ;
    
    mov dx, offset enter_y  ; ввод высоты
    mov ah, 09h             ;
    int 21h                 ;
    call getInt             ;
    mov y2, ax              ;
    
    mov dx, offset enter_col    ; ввод цвета
    mov ah, 9                   ;
    int 21h                     ;
    call getInt                 ;
    mov color, al               ;
    
    mov ah, 0       ; видеорежим = 13h (графика, 256, 320х200)
    mov al, 13h     ; 
    int 10h         ;
       
    mov cx, x1      ; текущая координата Х
    mov dx, y1      ; текущая координата Y
    mov ah, 0ch     ; функция установки пикселя
    mov bh, 0       ; видеостраница - 0
    mov al, color   ; установить цвет линий  
        
    c1:                 
        int 10h        ; установка пикселя
        cmp dx, y2     ; заполнение по высоте (Y)
        jne lp1_y      ; 
        cmp cx, x2     ; заполнение по ширине (X)
        jne lp1_x      ; 
        jmp c1_end     ; выход из цикла
    
        lp1_y:
            inc dx  ; увеличить координату Y
            jmp c1  ; 
            
        lp1_x:
            inc cx  ; увеличить координату X
            jmp c1  ;   
    c1_end:
       
    c2:  
        int 10h         ; установка пикселя
        cmp dx, y1      ; заполнение по высоте (Y)
        jne lp2_y       ;
        cmp cx, x1      ; заполнение по ширине (X)
        jne lp2_x       ;
        jmp c2_end      ; выход из цикла
    
        lp2_y:
            dec dx  ; увеличить координату Y
            jmp c2  ;
        
        lp2_x:
            dec cx  ; увеличить координату X
            jmp c2  ;
    c2_end:    
    
    mov ah, 01h     ;
    int 21h         ; ожидание отклика
    mov ax, 4c00h   ;
    int 21h         ; конец программы     
       
    ; Ввод целого числа       
    getInt proc  
        mov ah, 0ah         ; команда считывания строки в буфер
        mov dx, offset buff ; адрес буфера
        int 21h             ;
         
        mov ah, 02h         ; переход на новую строку
        mov dl, 0dh         ; символ абзаца
        int 21h             ;  
        mov dl, 0ah         ; символ новой строки
        int 21h             ; 
        
        ; обработка содержимого буфера
        mov si, offset buff + 2 ; адрес начала строки
        mov ax, 0               ; итоговое целое число
        mov bx, 10              ; основание сc
        
        check_next:
            mov cl, [si] ; рассматриваемый символ буфера
            cmp cl, 0dh  ; проверка окончания буфера
            jz endin     ;
            
            cmp cl, '0'  ; ошибка если символ <0 
            jb err
            cmp cl, '9'  ; ошибка если символ >9
            ja err
         
            sub cl, '0'  ; преобразование символа в число
            mul bx       ; умножение ax на 10
            add ax, cx   ; прибавление нового разряда
            inc si       ; следующий символ
        jmp check_next   ; 
     
        err: 
            mov dx, offset error    ; 
            mov ah, 09h             ;
            int 21h                 ; вывод сообщения об ошибке
            mov ax, 4c01h           ;
            int 21h                 ; завершение программы
     
        endin:
            ret ; конец обработки буфера  
    getInt endp   
ends

end start
