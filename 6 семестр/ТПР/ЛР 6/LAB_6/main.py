import numpy as np

# вывод матрицы
def print_matrix(A):
    for row in A:
        for x in row:
            print('%.2f' % x, end=' ')
        print()
    print()


def print_w(W, i, j):
    print('w%i%i = ( ' % (i, j), end='')
    for wi in W:
        print('%.2f; ' % wi, end='')
    print(')')


# получение собственного вектора матрицы
def get_W(A):
    n = len(A)
    W = [0] * n

    for j in range(n):
        for i in range(n):
            W[j] += A[i][j]
        W[j] = 1 / W[j]

    s = sum(W)
    return list(map(lambda x: x / s, W))


# матрица парных сравнений влияния свойств на цель
A1 = [[1, 1/2, 6, 2],
      [2, 1, 3, 4],
      [1/6, 1/3, 1, 1/3],
      [1/2, 1/4, 3, 1]]

# матрицы парных сравнений наличия свойств у решений
A21 = [[1, 1/3, 1/2],
       [3, 1, 3],
       [2, 1/3, 1]]

A22 = [[1, 1, 1],
       [1, 1, 1],
       [1, 1, 1]]

A23 = [[1, 5, 1],
       [1/5, 1, 1/5],
       [1, 5, 1]]

A24 = [[1, 9, 7],
       [1/9, 1, 1/5],
       [1/7, 5, 1]]

A = [[A1], [A21, A22, A23, A24]]                    # матрицы парных сравнений
w = [[[0] * len(A1)], [[0] * len(A21)] * len(A1)]   # значения функции приоритетов
D = [0] * len(A21)                                  # характеристики решений


for i in range(2):
    for j in range(len(A[i])):
        n = len(A[i][j])

        print('Матрица парных сравнений A%i%i:' % (i+1, j+1))
        print_matrix(A[i][j])

        W = np.array(get_W(A[i][j]))
        print_w(W, i+1, j+1)

        W1 = np.dot(A[i][j], W) / W
        l = sum(map(lambda x: x / n, W1))
        print('λ = %.2f' % l)

        IS = (l - n) / (n - 1)
        print('ИС = %.3f' % IS)

        if abs(n - l) < 1:
            print('Матрица согласована')
            w[i][j] = list(W)
        else:
            print('Матрица плохо согласована')
            exit()

        print()

for i in range(len(A21)):
    for j in range(len(A1)):
        D[i] += w[0][0][j] * w[1][j][i]
    print('D%i = %.2f' % (i+1, D[i]))

D = np.array(D)
index_max = np.argmax(D) + 1
print('Наиболее предпочтительное решение - %i' % index_max)
