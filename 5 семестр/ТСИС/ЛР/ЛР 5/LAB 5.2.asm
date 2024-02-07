data segment
    MAS1 DW 10 DUP(0)   ; ������ ������
    MAS2 DW 10 DUP(0)   ; ������ ������
    size DW 10          ; ������ ��������
    first DW 1          ; ������ ������� MAS1
    step DW 2           ; ��� ���������� MAS1
    searched DW 9       ; ������� �������
    index DW ?          ; ������ �������� ��������
    sum DW ?            ; ����� ��������� ������� 
ends

stack segment
    dw 128 dup(0)
ends

code segment
start:
    ; ������������� �������� ���������
    mov ax, data
    mov ds, ax
    mov es, ax

    ; ��� ���������
    CALL fill_array
    CALL copy_array
    CALL search_element
    CALL sum_array
      
    ; ���������         
    MOV AX, 4C00h
    INT 21h
    
    ; ���������� MAS1
    fill_array PROC
        MOV CX, size    ; ������� ����� �������
        MOV DX, first   ; ������� ����������
        LEA BX, MAS1    ; ����� �������� �������
        
        fill_loop:
        MOV [BX], DX   
        ADD DX, step    
        ADD BX, 2        
        LOOP fill_loop
        
        RET
    fill_array ENDP
    
    ; ����������� MAS1 � MAS2
    copy_array PROC
        LEA SI, MAS1    ; �����-��������
        LEA DI, MAS2    ; ����c-�������
        MOV CX, size    ; ������� ����� �������
        CLD             ; ����� ����� D
        REP MOVSW       ; ������� �������
        RET
    copy_array ENDP
    
    ; ����� ������� 
    search_element PROC
        LEA DI, MAS1            ; ����� ������ �������
        LEA SI, [searched + 2]  ; ����� �������� ��������   
        MOV index, -1           ; �������� �������
        MOV CX, size            ; ������� ����� �������
        
        search_loop:
        SUB SI, 2
        INC index              
        CMPSW    
        JZ search_end      ; ������� ������          
        LOOP search_loop        
        MOV index, -1      ; ������� �� ������         
        
        search_end:
        RET
    search_element ENDP
    
    ; ����� MAS1
    sum_array PROC
        MOV sum, 0      ; ����� ���������
        LEA SI, MAS1    ; ����� ������ �������
        MOV CX, size    ; ������� ����� �������
        
        sum_loop:
        MOV AX, [SI]
        ADD [sum], AX
        ADD SI, 2
        LOOP sum_loop
        
        RET
    sum_array ENDP
ends

end start


