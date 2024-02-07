; ������� ����������� ����������
data segment
    v dw 12345
    pkey db 13, 10, 'Press any key...$'
ends

; ������� �����
stack segment
    dw 128 dup(0)
ends
 
; ������� ������������ ����
code segment
start:
    mov ax, data        ; ������������� �������� ���������
    mov ds, ax          ;
    mov es, ax          ;

    mov bx, v           ; BX = v
    mov ah, 02h         ; ��� ������� DOS 02h - ����� �������
    mov cx, 16          ; ������������� �������� �����
    
    lp:
    shl bx, 1           ; ����� BX �� 1 ��� �����
    mov dl, '0'         ; dl = '0'
    jnc print           ; �������, ���� ���������� ��� ����� 0
    inc dl              ; ����� dl = dl + 1 = '1'
    print:
    int 21h             ; ����� ������� DOS 02h (����� ������� dl)
    loop lp             ; ����� �������� ����� (���� cx != 0)
            
    lea dx, pkey        ; ������������� ����� ������ pkey
    mov ah, 09h         ; ��� ������� DOS 09h - ����� ������
    int 21h             ; ����� ������ 'Press any key...'
     
    mov ah, 01h         ; ��� ������� DOS 01h - �������� �������
    int 21h             ; ������� � ����� ��������
    
    mov ah, 4Ch         ; ��� ������� DOS 4Ch - �������� ���������� ��
    int 21h             ; ����� ������� DOS 4C, ���������� ���������
ends

end start
