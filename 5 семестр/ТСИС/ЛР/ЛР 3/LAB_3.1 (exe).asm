; ������� ����������� ����������
data segment
    pkey db 13, 10, "Press any key...$"
    alpha dw 25     
    beta dw 32      
    hello db 'Privet kafedra IS!$'
ends

; ������� �����
stack segment
    dw 128 dup(0)
ends

; ������� ������������ ���� 
code segment
start:
    mov ax, data            ; ������������� �������� ���������
    mov ds, ax              ;
    mov es, ax              ;
    
    mov ax, 0255        	; ��������� �������� 255 � ������� AX
    inc ax                  ; ��������� �������� AX �� 1
    add ax, alpha           ; �������� �������� alpha � AX
    nop                 	; ������ �� ������
    mov bx, ax        	    ; ��������� �������� AX � �������� BX
    dec bx              	; ��������� �������� BX �� 1
    sub bx, beta        	; ������� �������� beta �� BX
    mov dx, bx           	; ��������� �������� BX � �������� DX
    sub dx, 10          	; ������� 10 �� �������� DX
    xchg ax, dx        	    ; �������� �������� AX � DX �������
    push bx            	    ; ��������� �������� BX � ����
    push ax            	    ; ��������� �������� AX � ����
    pop cx           	    ; ������� �������� �� ����� � CX
    mov si, cx         	    ; ��������� �������� CX � �������� SI
    mov di, dx          	; ��������� �������� DX � �������� DI
    mov [0150h], cx     	; ��������� �������� CX � ������ ������ 0150h
    shl ax, 2          	    ; �������� ���� � AX �� 2 ������� �����
    
    mov dx, offset hello    ; ��������� �������� ������ hello � DX
    mov ax, 0900h   	    ; ������� DOS - ����� ������
    int 21h            	    ; ������� ���������� 21h (������� ������ hello)  
    
    lea dx, pkey            ; ��������� �������� ������ pkey � DX
    mov ax, 0900h           ; ������� DOS - ����� ������
    int 21h                 ; ������� ���������� 21h (������� ������ pkey)
      
    mov ah, 1               ; ������� DOS - �������� ������� �������
    int 21h                 ; ������� ���������� 21h (����� ��������)
    
    mov ax, 4c00h		    ; ������� DOS - �������� ���������� ��
    int 21h			        ; ������� ���������� 21h (������� ���������� ��)   
ends

end start
