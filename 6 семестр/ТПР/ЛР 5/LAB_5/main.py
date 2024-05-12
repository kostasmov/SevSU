# проверка доминирования x1 над x2
def is_preferable(x1, x2):
    # проверка что все fi(x1) >= fi(x2)
    all_greater_or_equal = all(fx1 >= fx2 for fx1, fx2 in zip(x1, x2))

    # проверка что хотя бы один fj(x1) != fj(x2)
    at_least_one_not_equal = any(fx1 != fx2 for fx1, fx2 in zip(x1, x2))

    return all_greater_or_equal and at_least_one_not_equal


# вывод таблицы векторных критериев
def print_table(x, f=[]):
    # заголовки столбцов
    print('    ', end='')
    for i in range(len(x[0])):
        if i not in f:
            print(' K%i' % (i + 1), end='  ')
        else:
            print('  K%i' % (i + 1), end='   ')
    print()

    # строки таблицы
    for i, row in enumerate(x):
        if not row:
            continue
        print('x%i' % (i+1), end=' | ')
        for j, item in enumerate(row):
            if j not in f:
                print('%2i' % item, end=' | ')
            else:
                print('%3.2f' % item, end=' | ')
        print()
    print()


# вывод несравнимых решений
def print_C(C, n):
    print("C" + "'" * n + "(X) = { ", end='')
    for i in C:
        print('x%i' % (i + 1), end=', ')
    print('}\n')


# формирование множества несравнимых решений
def get_CX(x):
    C = []

    for j in range(len(x)):
        if not x[j]:
            continue

        if len(C) == 0:
            C.append(j)
            continue

        on_delete = []

        for i in C:
            if is_preferable(x[i], x[j]):
                break
            elif is_preferable(x[j], x[i]):
                on_delete += [i]
        else:
            C.append(j)
            for index in on_delete:
                C.remove(index)

    return C


# ВЫЧИСЛЕНИЯ

# множество решений
x = [[3, 5, 5, 4, 4],
     [4, 4, 4, 5, 4],
     [5, 4, 3, 3, 5],
     [3, 5, 3, 5, 3],
     [4, 2, 4, 5, 5],
     [3, 5, 3, 5, 3],
     [5, 3, 4, 3, 4],
     [4, 5, 3, 4, 3]]

# параметры уступок и приращения
W = (((1, 2), (2, 1)),
     ((4, 1), (5, 2)))

print_table(x)

# индексы несравнимых решений
C_x = get_CX(x)
print_C(C_x, 0)

indexes = []

# подсчёт коэффициентов относительной важности
for iter, w in enumerate(W):
    wi = w[0][1]
    wj = w[1][1]

    i = w[0][0] - 1
    j = w[1][0] - 1

    print('w%i = %i, w%i = %i' % (i + 1, wi, j + 1, wj))

    if wi > wj:
        c = i
        i = j
        j = c

        c = wi
        wi = wj
        wj = c

    # коэффициент относительной важности
    theta = wj / (wj + wi)
    print("Θ = %.3f" % theta, end='\n\n')

    table = [x[i].copy() if i in C_x else [] for i in range(len(x))]

    for index, K in enumerate(x):
        if table[index]:
            table[index][j] = round(theta * K[i] + (1 - theta) * K[j], 3)

    indexes.append(j)

    print_table(table, indexes)
    C_x = get_CX(table)
    print_C(C_x, iter+1)

    x = table
