import numpy as np


# вывод матрицы
def print_matrix(a):
    for row in a:
        print(' '.join('%2i' % x for x in row))
    print()


# нахождение коэффициента потерь
def find_p(A, i, j, index):
    p = 0

    for k in range(len(A)):
        if k == index:
            continue
        p += abs(A[index][i][j] - A[k][i][j])

    return int(p)


# вывод итогового ранжирования
def print_R(Rl, Rr, end=False):
    print('R = { ', end='')

    Rl = sorted(Rl.items(), key=lambda item: item[1])
    Rr = sorted(Rr.items(), key=lambda item: item[1])

    for item in Rl:
        print('x%i' % (item[0] + 1), end=' ')
    if end == False:
        print('... ', end='')
    for item in Rr:
        print('x%i' % (item[0] + 1), end=' ')
    print('}\n')


# итоговое ранжирование через алгоритм Кемени
def Kemeni(A, cols_i, rows_i, Rl={}, Rr={}, iter=1):
    n = A.shape[1]  # число решений
    m = A.shape[0]  # число ранжирований

    # проверка окончания для нечётного числа решений
    count = []
    for x in set(cols_i + rows_i):
        if x not in Rl.keys() and x not in Rr.keys():
            count.append(x)
    if len(count) == 1:
        max_key = max(Rl.values())
        Rl[count[0]] = max_key + 1

        print('Оставшееся решение - x%i\n' % (count[0]+1))
        return Rl, Rr

    # расчёт матрицы потерь
    P = np.zeros((n, n))
    for i in range(n):
          for j in range(n):
                r = [A[k][i][j] for k in range(m)]
                r_max_i = np.argmax(r)

                P[i][j] = find_p(A, i, j, r_max_i)

    # определение матрицы Q
    E = np.ones((n, n)) - np.eye(n)
    Q = np.dot(np.dot(E, P), E)

    min_val = np.inf
    min_index = None

    # поиск qmin
    for index in np.ndindex(Q.shape):
        i = rows_i[index[0]]
        j = cols_i[index[1]]

        if (all(x not in Rl.keys() and x not in Rr.keys() for x in (i, j))
                and i != j and Q[index] < min_val):
            min_val = Q[index]
            min_index = index

    # проверка окончания для чётного числа решений
    if not min_index:
        print('')
        return Rl, Rr


    # ВЫВОД ВЫЧИСЛЕНИЙ В ИТЕРАЦИИ

    print('-' * 5 + ' Итерация №%i ' % iter + '-' * 5, end='\n\n')

    for k in range(m):
        print('Ранжирование R%i:' % (k + 1))
        print_matrix(A[k])

    print('Матрица потерь P:')
    print_matrix(P)

    print('Матрица Q:')
    print_matrix(Q)

    i = rows_i[min_index[0]]
    j = cols_i[min_index[1]]

    print('qmin = %i' % min_val)

    # размещение альтернатив в итоговое ранжирование
    if not Rl:
        Rl[j] = 0
        Rr[i] = n-1
    else:
        max_key = max(Rl.values())
        min_key = min(Rr.values())
        Rl[j] = max_key + 1
        Rr[i] = min_key - 1

    print_R(Rl, Rr)

    # удаление лишних столбцов и строк
    new_A = np.empty((0, n-1, n-1))
    for k in range(m):
        a = np.delete(A[k], min_index[0], axis=0)
        a = np.delete(a, min_index[1], axis=1)
        new_A = np.concatenate((new_A, a[np.newaxis, :, :]), axis=0)

    cols_i.remove(j)
    rows_i.remove(i)

    return Kemeni(new_A, cols_i, rows_i, Rl, Rr, iter+1)


# исходные ранжирования
R = [
    [np.array([2, 4, 1, 3, 7, 5, 6]), []],
    [np.array([1, 7, 5, 4, 2, 6, 3]), [(1, 7), (4, 2)]],
    [np.array([3, 4, 6, 5, 2, 7, 1]), [(4, 6), (2, 7)]],
    [np.array([3, 4, 6, 2, 1, 7, 5]), [(3, 4), (6, 2)]],
    [np.array([3, 4, 6, 2, 1, 5, 7]), [(3, 4), (6, 2), (5, 7)]],
    [np.array([6, 4, 1, 2, 7, 5, 3]), [(6, 4), (1, 2)]],
    [np.array([7, 3, 4, 6, 2, 1, 5]), [(1, 5)]],
    [np.array([7, 3, 4, 6, 2, 1, 5]), [(7, 3), (1, 5)]]
]

# R = [
#     [np.array([2, 4, 1, 3]), []],
#     [np.array([1, 3, 4, 2]), [(3, 4)]],
#     [np.array([2, 3, 4, 1]), [(2, 3)]],
#     [np.array([3, 2, 1, 4]), [(1, 4)]]
# ]

A = []
n = len(R[0][0])    # число решений

# построение матрицы для каждого ранжирования
for k in range(len(R)):
    Rk = R[k]

    Ak = np.zeros((n, n))

    for h in range(n-1):
        for l in range(h+1, n):
            i = Rk[0][h] - 1
            j = Rk[0][l] - 1

            Ak[i][j] = 1
            Ak[j][i] = -1

    for eq in Rk[1]:
        i = eq[0] - 1
        j = eq[1] - 1

        Ak[i][j] = 0
        Ak[j][i] = 0

    A.append(Ak)

Rl, Rr = Kemeni(np.array(A), list(range(n)), list(range(n)))
print('Итоговое ранжирование:')
print_R(Rl, Rr, end=True)
