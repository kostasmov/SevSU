org 100h

; ��� ��������� 
mov cx, 0

mov dx, offset enter_x  ; ���� ������
mov ah, 09h             ;
int 21h                 ;
call getInt             ; 
mov x2, ax              ;

mov dx, offset enter_y  ; ���� ������
mov ah, 09h             ;
int 21h                 ;
call getInt             ;
mov y2, ax              ;

mov dx, offset enter_col    ; ���� �����
mov ah, 9                   ;
int 21h                     ;
call getInt                 ;
mov color, al               ;

mov ah, 0       ; ���������� = 13h (�������, 256, 320�200)
mov al, 13h     ; 
int 10h         ;
   
mov cx, x1      ; ������� ���������� �
mov dx, y1      ; ������� ���������� Y
mov ah, 0ch     ; ������� ��������� �������
mov bh, 0       ; ������������� - 0
mov al, color   ; ���������� ���� �����  
    
c1:                 
    int 10h        ; ��������� �������
    cmp dx, y2     ; ���������� �� ������ (Y)
    jne lp1_y      ; 
    cmp cx, x2     ; ���������� �� ������ (X)
    jne lp1_x      ; 
    jmp c1_end     ; ����� �� �����

    lp1_y:
        inc dx  ; ��������� ���������� Y
        jmp c1  ; 
        
    lp1_x:
        inc cx  ; ��������� ���������� X
        jmp c1  ;   
c1_end:
   
c2:  
    int 10h         ; ��������� �������
    cmp dx, y1      ; ���������� �� ������ (Y)
    jne lp2_y       ;
    cmp cx, x1      ; ���������� �� ������ (X)
    jne lp2_x       ;
    jmp c2_end      ; ����� �� �����

    lp2_y:
        dec dx  ; ��������� ���������� Y
        jmp c2  ;
    
    lp2_x:
        dec cx  ; ��������� ���������� X
        jmp c2  ;
c2_end:    

mov ah, 01h     ;
int 21h         ; �������� �������
mov ax, 4c00h   ;
int 21h         ; ����� ���������  
   
   
; ���� ������ �����       
getInt proc  
    mov ah, 0ah         ; ������� ���������� ������ � �����
    mov dx, offset buff ; ����� ������
    int 21h             ;
     
    mov ah, 02h         ; ������� �� ����� ������
    mov dl, 0dh         ; ������ ������
    int 21h             ;  
    mov dl, 0ah         ; ������ ����� ������
    int 21h             ; 
    
    ; ��������� ����������� ������
    mov si, offset buff + 2 ; ����� ������ ������
    mov ax, 0               ; �������� ����� �����
    mov bx, 10              ; ��������� �c
    
    check_next:
        mov cl, [si] ; ��������������� ������ ������
        cmp cl, 0dh  ; �������� ��������� ������
        jz endin     ;
        
        cmp cl, '0'  ; ������ ���� ������ <0 
        jb err
        cmp cl, '9'  ; ������ ���� ������ >9
        ja err
     
        sub cl, '0'  ; �������������� ������� � �����
        mul bx       ; ��������� ax �� 10
        add ax, cx   ; ����������� ������ �������
        inc si       ; ��������� ������
    jmp check_next   ; 
 
    err: 
        mov dx, offset error    ; 
        mov ah, 09h             ;
        int 21h                 ; ����� ��������� �� ������
        mov ax, 4c01h           ;
        int 21h                 ; ���������� ���������
 
    endin:
        ret ; ����� ��������� ������  
getInt endp   
   
     
; ����������
x1 dw 10                        ; ��������� ���������� x
y1 dw 10                        ; ��������� ���������� y
x2 dw 0                         ; ������ ��������������
y2 dw 0                         ; ������ ��������������
color db 10                     ; ���� �����
enter_x db '������� ������: $'  ;
enter_y db '������� ������: $'  ;
enter_col db '������� ����: $'  ;
error db '������������ ����! $' ; ��������� �� ������
buff db 4, ?, 4 dup(?)          ; ����� ��� ������ �����




