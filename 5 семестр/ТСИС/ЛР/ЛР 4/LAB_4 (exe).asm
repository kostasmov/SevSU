; �������� ����������
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
    mov ax, data   ; ������������� �������� ���������
    mov ds, ax     ;
    mov es, ax     ;           
        
    call f         ; ����� ������� �������� ���������
    mov ah, 4Ch    ; ������� DOS - �������� ���������� ��
    int 21h	       ; ����� ���������
    
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
    mov ans, ax    ; ���������� ������ � ans                    
    ret
f endp                       
ends  

end start
