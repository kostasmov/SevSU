c2 DW ?    ; ��������������� ���������� 

; ��������� �������� ���������
MOV AX, -3              
MOV BX, 10                 
MOV CX, 1           
    
CALL f         ; ����� ������� �������� ���������
MOV AH, 4Ch    ; ������� DOS - �������� ���������� ��
INT 21h	       ; ����� ���������                   

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
    MOV DX, AX  ; ���������� ������ � DX
    MOV BX, 0                     
    MOV CX, 0                    
    RET
f ENDP





