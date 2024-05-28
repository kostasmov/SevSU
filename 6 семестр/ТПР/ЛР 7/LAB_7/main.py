# вывод матрицы
def print_matrix(a):
    for row in a:
        for x in row:
            print('%2i' % x, end=' ')
        print()
    print()


# исходные ранжирования
R1 = [[2, 4, 1, 3, 7, 5, 6],
      []]

R2 = [[1, 7, 5, 4, 2, 6, 3],
      [(1, 7), (4, 2)]]

R3 = [[3, 4, 6, 5, 2, 7, 1],
      [(4, 6), (2, 7)]]

R4 = [[3, 4, 6, 2, 1, 5, 7],
      [(3, 4), (6, 2), (5, 7)]]

R5 = [[6, 4, 1, 2, 7, 5, 3],
      [(6, 4), (1, 2)]]

R6 = [[7, 3, 4, 6, 2, 1, 5],
      [(1, 5)]]

R7 = [[7, 3, 4, 6, 2, 1, 5],
      [(7, 3), (1, 5)]]

R = [R1, R2, R3, R4, R5, R6, R7]
A = []

# построение матрицы для каждого ранжирования
for k in range(len(R)):
      Rk = R[k]

      n = len(Rk[0])
      Ak = [[0] * n for _ in range(n)]

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

for a in A:
      print_matrix(a)