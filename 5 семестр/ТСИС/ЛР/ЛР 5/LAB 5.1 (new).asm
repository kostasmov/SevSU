; multi�segment executable file template.
data segment
    NAME1 DB 'ABCDEFGHI'
    NAME2 DB 'JKLMNOPQR'
    NAME3 DB 'STUVWXYZ*'
ends

stack segment
    dw 128 dup(0)
ends

code segment
start:
    ; set segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax
    
    ; add your code here
    LEA SI, NAME1   ; ������������� �������
    LEA DI, NAME2   ; NAME1 � NAME2
    MOV CX, 09      ; ��������� 9 ��������
    REP MOVSB
    
    LEA SI, NAME2   ; ������������� �������
    LEA DI, NAME3   ; NAME2 � NAME3
    MOV CX, 09      ; ��������� 9 ��������
    REP MOVSB
                    
    mov ax, 4c00h   ; exit to operating system.
    int 21h
ends

end start ; set entry point and stop the assembler.
