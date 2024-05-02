from math import sqrt


# проверка доминирования x1 над x2
def is_preferable(x1, x2):
    # проверка что все fi(x1) >= fi(x2)
    all_greater_or_equal = all(fx1 >= fx2 for fx1, fx2 in zip(x1, x2))

    # проверка что хотя бы один fj(x1) != fj(x2)
    at_least_one_not_equal = any(fx1 != fx2 for fx1, fx2 in zip(x1, x2))

    return all_greater_or_equal and at_least_one_not_equal


# ВЫЧИСЛЕНИЯ

# множество решений
x = [(3, 2, 2),
     (5, 6, 4),
     (5, 3, 3),
     (8, 4, 4),
     (6, 2, 6),
     (3, 8, 5),
     (6, 4, 3),
     (2, 5, 2),
     (9, 2, 5),
     (3, 5, 2)]

n = len(x)      # число решений
m = len(x[0])   # число частных критериев

# векторный критерий
f = [[x[i][j] for i in range(n)] for j in range(m)]

y = []  # значения векторного критерия
P = []  # множество Парето

# формирование множества Парето-оптимальных решений
for j in range(n):
    if len(P) == 0:
        P.append(j)
        continue

    on_delete = []

    for i in P:
        if is_preferable(x[i], x[j]):
            break

        if is_preferable(x[j], x[i]):
            on_delete += [i]
    else:
        P.append(j)
        for index in on_delete:
            P.remove(index)

# точка утопии
f_max = []
for i in range(m):
    f_max.append(max(f[i]))

# метрики от Парето-оптимальных решений до точки утопии
R = {}
for i in P:
    metric = 0
    for j in range(m):
        metric += (f_max[j] - x[i][j]) ** 2

    R[i] = sqrt(metric)

# эффективное решение
x_opt = min(R, key=R.get) + 1


# ВЫВОД ДАННЫХ

# входные данные: решения и частные критерии
print('      f1   f2   f3  ')
for i in range(n):
    print('x%-2i | %2i | %2i | %2i |' % (i+1, f[0][i], f[1][i], f[2][i]))
print()

# множество Парето
print('P(X) = { ', end='')
for i in P:
    print('x%i' % (i+1), end=', ')
print('}\n')

print('Точка утопии: (', end='')
for i in range(m):
    print(f_max[i], end=', ' if i < (m-1) else ')\n')
print()

print('Расстояния от решений до точки утопии:')
for i, r in R.items():
    print('r_x%i = %.3f' % (i+1, r))
print()

print('Эффективное решение: x%i' % x_opt)