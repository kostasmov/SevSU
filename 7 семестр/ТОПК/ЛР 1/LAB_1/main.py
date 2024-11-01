# таблица переходов
transitions = [
    [None, 2, None, None, 5, None, 7, None, 5],
    [None, 6, 3, 8, 5, 4, 7, 6, 8],
    [1, None, None, None, 5, None, None, None, 5]
]

# множество заключительных состояний КА
F = [1, 3, 5, 7, 8]


def validate(string):
    print(f'\nВходная строка - {string}')

    q = 0   # начальное состояние

    # проходим по каждому символу строки, пока не достигнем конца или недопустимого состояния
    for s in string:
        if s == 'a':
            q = transitions[0][q]
        elif s == 'b':
            q = transitions[1][q]
        elif s == 'c':
            q = transitions[2][q]
        else:
            q = None

        # print(s, q)
        if q == None:
            # print(f'{s} - недопустимый символ')
            break
        # else:
        #     print(f'{s} - допустимый символ')

    if q == None:
        print('СТРОКА НЕДОПУСТИМА')
    elif q in F:
        print('СТРОКА ДОПУСТИМА')
    else:
        print('СТРОКА НЕДОПУСТИМА (преждевременное окончание)')


# ОСНОВНОЙ КОД
print('Регулярное выражение - CA{B}B{BA˅BB˅BC} ˅ C{BB˅BA}')
try:
    with open("input.txt", "r") as file:
        for line in file:
            validate(line.strip())
except FileNotFoundError:
    print("Файл не найден")