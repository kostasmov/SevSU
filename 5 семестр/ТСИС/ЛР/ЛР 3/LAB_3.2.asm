org 100h            ; ��������� ���������� � ������ 100h
jmp start           ; ����������� ������� �� ����� start
;-- ������ ------------------------------------------------------------
v dw 12345
pak db 13, 10, 'Press any key...$'
;----------------------------------------------------------------------
start:
mov bx, v           ; BX = v
mov ah, 2           ; ������� DOS 02h - ����� �������
mov cx, 16          ; ������������� �������� �����
;
lp:
shl bx, 1           ; ����� BX �� 1 ��� �����
mov dl, '0'         ; dl = '0'
jnc print           ; �������, ���� ���������� ��� ����� 0
inc dl              ; dl = dl + 1 = '1'
print:
int 21h             ; ��������� � ������� DOS 02h
loop lp             ; ������� �����
;
mov ah, 9           ; \
mov dx, offset pak  ; > ����� ������ 'Press any key...'
int 21h             ; /
mov ah, 8           ; \
int 21h             ; / ���� ������� ��� ���
mov ax, 4C00h       ; \
int 21h             ; / ���������� ���������
