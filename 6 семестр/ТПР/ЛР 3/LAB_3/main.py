import numpy as np
import matplotlib.pyplot as plt


# значение аддитивной функции полезности по трём критериям
def findU(k1, k2, k3):
    u1 = a[0] * k1 + b[0]
    u2 = a[1] * k2 + b[1]
    u3 = a[2] * k3 + b[2]

    return u1 + u2 + u3


# множество решений
X = [(40, 50, 30),
     (80, 30, 50),
     (50, 90, 45),
     (75, 40, 60),
     (60, 80, 40)]

# дискретные значения критериев
K1 = [20, 40, 60, 80, 100]
K2 = [20, 40, 60, 80, 100, 120]
K3 = [20, 30, 40, 50, 60, 70]

K = [K1, K2, K3]                # множество критериев
inverted = [False, True, True]  # "обратность" критериев

n = len(X)  # число решений
m = len(K)  # число критериев

crit_names = ['Качество дачи', 'Расстояние до города', 'Цена']

a, b = list(), list()   # значения a, b для Ui=ai*ki+bi

# вычисление коэффициентов одномерных Ui и вывод графиков
for i in range(len(K)):
    x = np.array(K[i].copy())
    y = np.array([i for i in range(len(K[i]))])

    if inverted[i]:
        x = x[::-1]

    subplot = plt.subplot(3, 1, i+1)

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x * y)
    sum_x_sq = sum(x ** 2)

    # метод наименьших квадратов
    a_i = (len(x) * sum_xy - sum_x * sum_y) / (len(x) * sum_x_sq - (sum_x ** 2))
    b_i = (sum_y - a_i * sum_x) / len(x)

    a.append(a_i)
    b.append(b_i)

    x_s = np.linspace(x[0], x[-1])

    # формирование подграфика
    subplot.title.set_text("U%i:%10.3f*k+%10.3f" % (i+1, a_i, b_i))
    subplot.plot(x_s, a_i * x_s + b_i)
    subplot.plot(x, y, '.', markersize=5)

    subplot.set_xlabel(crit_names[i])
    subplot.set_ylabel('U%i' % (i+1))

    for y_i in y:
        subplot.axhline(y=y_i, linestyle='--', alpha=0.2)

    subplot.set_xticks(x)
    subplot.set_yticks(y)

plt.subplots_adjust(hspace=1.2)
plt.show()

Uk = [[] for _ in range(m)]     # одномерные полезности
U = [0 for _ in range(n)]       # многомерная полезность

# значения многомерной полезности
for i in range(n):
    for j in range(m):
        result = a[j] * X[i][j] + b[j]
        Uk[j].append(result)
        U[i] += result


# ВЫВОД РЕЗУЛЬТАТОВ

# входные данные: решения и частные критерии
print('     k1   k2   k3    U1     U2     U3      U  ')
for i in range(n):
    print('x%i | %2i | %2i | %2i | %.2f | %.2f | %.2f | %.2f |' %
          (i+1, X[i][0], X[i][1], X[i][2], Uk[0][i], Uk[1][i], Uk[2][i], U[i]))
print()

# матрицы предпочтения
for k3 in K3:
    print('k3 = %i' % k3)
    for k2 in K2[::-1]:
        for k1 in K1:
            print('%2.0f' % findU(k1, k2, k3), end=' ')
        print()
    print()
