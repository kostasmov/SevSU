data segment
    MAS1 DW 10 DUP(0)   ; первый массив
    MAS2 DW 10 DUP(0)   ; второй массив
    size DW 10          ; размер массивов
    first DW 1          ; первый элемент MAS1
    step DW 2           ; шаг заполнения MAS1
    searched DW 9       ; искомый элемент
    index DW ?          ; индекс искомого элемента
    sum DW ?            ; сумма элементов массива 
ends

stack segment
    dw 128 dup(0)
ends

code segment
start:
    ; инициализация адресных регистров
    mov ax, data
    mov ds, ax
    mov es, ax

    ; КОД ПРОГРАММЫ
    CALL fill_array
    CALL copy_array
    CALL search_element
    CALL sum_array
      
    ; ФИНАЛОЧКА         
    MOV AX, 4C00h
    INT 21h
    
    ; Заполнение MAS1
    fill_array PROC
        MOV CX, size    ; счётчик длины массива
        MOV DX, first   ; элемент заполнения
        LEA BX, MAS1    ; адрес элемента массива
        
        fill_loop:
        MOV [BX], DX   
        ADD DX, step    
        ADD BX, 2        
        LOOP fill_loop
        
        RET
    fill_array ENDP
    
    ; Копирование MAS1 в MAS2
    copy_array PROC
        LEA SI, MAS1    ; адрес-источник
        LEA DI, MAS2    ; адреc-приёмник
        MOV CX, size    ; счётчик длины массива
        CLD             ; сброс флага D
        REP MOVSW       ; перенос массива
        RET
    copy_array ENDP
    
    ; Поиск индекса 
    search_element PROC
        LEA DI, MAS1            ; адрес ячейки массива
        LEA SI, [searched + 2]  ; адрес искомого элемента   
        MOV index, -1           ; значение индекса
        MOV CX, size            ; счётчик длины массива
        
        search_loop:
        SUB SI, 2
        INC index              
        CMPSW    
        JZ search_end      ; элемент найден          
        LOOP search_loop        
        MOV index, -1      ; элемент не найден         
        
        search_end:
        RET
    search_element ENDP
    
    ; Сумма MAS1
    sum_array PROC
        MOV sum, 0      ; сумма элементов
        LEA SI, MAS1    ; адрес ячейки массива
        MOV CX, size    ; счётчик длины массива
        
        sum_loop:
        MOV AX, [SI]
        ADD [sum], AX
        ADD SI, 2
        LOOP sum_loop
        
        RET
    sum_array ENDP
ends

end start


