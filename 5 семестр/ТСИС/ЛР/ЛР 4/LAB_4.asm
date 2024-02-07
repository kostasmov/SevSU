c2 DW ?    ; вспомогательная переменная 

; установка значений регистров
MOV AX, -3              
MOV BX, 10                 
MOV CX, 1           
    
CALL f         ; вызов функции подсчёта выражения
MOV AH, 4Ch    ; функция DOS - передача управления ОС
INT 21h	       ; конец программы                   

f PROC
    MOV c2, CX         
    SAL AX, 1   ; A *= 2    
    SUB CX, AX  ; C = C - A   
    MOV AX, CX  ; A = C 
    MOV CX, 3   ; C = 3                  
    IMUL CX     ; A *= 3                  
    SUB BX, c2  ; B = B - C           
    INC BX      ; B += 1              
    SAR BX, 1   ; B /= 2         
    ADD AX, BX  ; A = A + B                  
    MOV DX, AX  ; сохранение ответа в DX
    MOV BX, 0                     
    MOV CX, 0                    
    RET
f ENDP





