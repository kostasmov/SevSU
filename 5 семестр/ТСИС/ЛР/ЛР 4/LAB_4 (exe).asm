; значения параметров
data segment
    a dw -3
    b dw 10
    c dw 1
    ans dw ?    
ends

stack segment
    dw 128 dup(0)
ends

code segment
start:
    mov ax, data   ; инициализация адресных регистров
    mov ds, ax     ;
    mov es, ax     ;           
        
    call f         ; вызов функции подсчёта выражения
    mov ah, 4Ch    ; функция DOS - передача управления ОС
    int 21h	       ; конец программы
    
    f proc
    mov ax, a      ; AX = A
    mov bx, b      ; BX = B
    mov cx, c      ; CX = C
       
    sal ax, 1      ; AX *= 2    
    sub cx, ax     ; CX = CX - AX   
    mov ax, cx     ; AX = C 
    mov cx, 3      ; CX = 3                  
    imul cx        ; AX *= 3                  
    sub bx, c      ; BX = BX - C           
    inc bx         ; B += 1              
    sar bx, 1      ; B /= 2         
    add ax, bx     ; AX = AX + BX                  
    mov ans, ax    ; сохранение ответа в ans                    
    ret
f endp                       
ends  

end start
