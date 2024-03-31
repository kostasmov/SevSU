import copy

# упорядочение по матрице отношений
def collate_classes(a, n):
    MaxR = [0] * n  # массив упорядоченных классов
    K = 0
    K1 = 0
    count = n

    while count > 0:
        done = 0
        # определение исключаемых элементов
        for i in range(n):
            row_sum = sum(a[i])
            if row_sum == 0:
                MaxR[K] = i
                K += 1
                done += 1

        if not done:
            return 0

        # обнуление отношений с исключаемыми элементами
        for q in range(K1, K):
            for x in range(n):
                a[x][MaxR[q]] = 0

        # исключение элементов, добавленных в MaxR
        for q in range(K1, K):
            for x in range(n):
                a[MaxR[q]][x] = 1
        K1 = K
        count = n - K

    MaxR.reverse()
    return MaxR


# A = [
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
# ]

n = 7  # число альтернатив

# A = [
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
# ]

A = [
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1]
]

R = [[] for _ in range(n)]  # множества экв. элементов
K = []                      # классы эквивалентности
Uk = []                     # функция полезности для классов
Ux = [0] * n                # функция полезности для альтернатив


# ВЫЧИСЛЕНИЯ

# заполнение множеств экв. элементов
for i in range(n):
    for j in range(n):
        if A[i][j] == A[j][i] == 1:
            R[i].append(j)

# идентификация классов эквивалентности
K = list(sorted(set(tuple(r) for r in R)))

# заполнение матрицы отношений классов эквивалентности
B = [[0] * len(K) for _ in range(len(K))]
for l in range(len(K)):
    for h in range(len(K)):
        if l == h:
            continue
        summ = sum(A[i][j] for i in K[l] for j in K[h])
        if summ != 0:
            B[l][h] = 1

indexes = [i for i in range(len(K))]
# indexes = collate_classes(copy.deepcopy(B), len(B))
# if indexes == 0:
#     print("ОШИБКА: множество X не может быть упорядочено")
#     exit()

print(K)
print(B)
print(indexes)

# поиск значений U(k) для классов экв-ти
Uk = [0] * len(K)
for index in range(1, len(indexes)):
    m = indexes[index]
    h = {indexes[i] for i in range(index) if B[indexes[i]][m] == 1}
    l = {indexes[i] for i in range(index) if B[m][indexes[i]] == 1}
    print(h, l)
    if l != set() and h == set():
        Uk[m] = index + 1
    elif l == set() and h != set():
        Uk[m] = -(index + 1)
    elif l == set() and h == set():
        print("ОШИБКА: имеется несвязанное решение x{}".format(m+1))
        exit()
    else:
        Uk[m] = (Uk[max(l)] + Uk[min(h)]) / 2
    print(Uk)

# Uk = [0] * len(K)
# for m in range(1, len(K)):
#     h = {i for i in range(m) if B[i][m] == 1}
#     l = {i for i in range(m) if B[m][i] == 1}
#     if l != set() and h == set():
#         Uk[m] = m + 1
#     elif l == set() and h != set():
#         Uk[m] = -(m + 1)
#     elif l == set() and h == set():
#         print("Ошибка: несвязанное решение", m)
#         exit()
#     else:
#         Uk[m] = (Uk[max(l)] + Uk[min(h)]) / 2
#         if Uk[max(l)] > Uk[min(h)]:
#             print("ОШИБКА: множество X не может быть упорядочено")
#             exit()

for l in range(len(Uk)):
    for i in K[l]:
        Ux[i] = Uk[l]


# ВЫВОД ДАННЫХ

print("Матрица нестрогого предпочтения:")
for row in A:
    print(*row)
print()

print("Множества эквивалентных элементов:")
for i in range(n):
    print("R(x{}) = {{".format(i + 1), end="")
    for j in R[i]:
        print(" x{}".format(j + 1), end=",")
    print("}")
print()

print("Классы эквивалентности X/~:")
for l in range(len(K)):
    print("k{} -> {{".format(l + 1), end="")
    for i in K[l]:
        print(" x{}".format(i + 1), end=",")
    print("}")
print()

print("Полезность классов эквивалентности:")
for l in range(len(K)):
    print("U(k{}) = {}".format(l + 1, Uk[l]))
print()

print("Полезность альтернатив:")
for i in range(n):
    print("U(x{}) = {}".format(i + 1, Ux[i]))
print()

print("Эффективные решения:")
print("{", end="")
for i in range(n):
    if Ux[i] == max(Ux):
        print(" x{}".format(i + 1, Ux[i]), end=",")
print("}")