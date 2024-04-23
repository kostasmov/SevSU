import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import pprint
# from pylab import *
# from scipy.linalg import *
# from operator import itemgetter

# class SquareFunction:
#
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c
#
#     def get_value(self, x):
#         return self.a * (x**2) + self.b * x + self.c


# дискретные значения критериев
K1 = [20, 40, 60, 80, 100]
K2 = [20, 40, 60, 80, 100, 120]
K3 = [20, 30, 40, 50, 60, 70]

K = [K1, K2, K3]
inverted = [False, True, True]
crit_names = ['Качество дачи', 'Расстояние до города', 'Цена']

fig, axs = plt.subplots(3, 1)

for i in range(len(K)):
    x = np.array(K[i].copy())
    y = np.array([i for i in range(len(K[i]))])

    if inverted[i]:
        x = 1 / x

    subplot = plt.subplot(3, 1, i+1)

    m = np.vstack((x**2, x, np.ones(len(x)))).T
    a, b, k = np.linalg.lstsq(m, y, rcond=None)[0]

    x_s = np.linspace(x[0], x[-1])

    subplot.title.set_text("U%i:%10.3f*x^2+%10.3f*x+%10.3f" % (i+1, a, b, k))
    subplot.plot(x_s, a*(x_s**2) + b*x_s + k)
    subplot.plot(x, y, '.', markersize=5)

    subplot.set_xlabel(crit_names[i])
    subplot.set_ylabel('U%i' % (i+1))
    #
    # subplot.set_xticks(x)
    # subplot.set_yticks(y)

fig.subplots_adjust(hspace=1.2)

plt.show()

# x_plot = np.linspace(min(x), max(x), 100)
# y_plot = a * x_plot + b * (x_plot ** 2)
#
# subplot = plt.subplot(3, 1, i + 1)
# plt.plot(x_plot, y_plot, color='r', label=crit_names[i])


# for c in range(criterias_count):
#     criteria = {}
#     criteria['name'] = input_file.readline().strip()
#     criteria['values'] = list(map(lambda x: float(x), input_file.readline().split(' ')))
#     if input_file.readline().strip() == 'inverted':
#         criteria['values'] = list(map(lambda x: 1 / x, criteria['values']))
#         criteria['inverted'] = True
#     else:
#         criteria['inverted'] = False
#
#     # calculate criteria profitability function
#     subplot = plt.subplot(3, 1, c + 1)
#     x = np.array(criteria['values'])
#     y = np.array([i for i in range(len(x))])
#     m = vstack((x**2, x, ones(len(x)))).T
#     a, b, k = lstsq(m, y)[0]
#     x_s = linspace(x[0], x[-1])
#     subplot.title.set_text("%s: %10.4f*x^2+%10.4f*x+%10.4f" % (criteria['name'], a, b, k))
#     subplot.plot(x_s, a*(x_s**2) + b*x_s + k, '--')
#     subplot.plot(x, y, '.', markersize = 4)
#     criteria['function'] = SquareFunction(a, b, k)
#
#     criterias.append(criteria)
#
# plt.show()
#
# alternatives_count = int(input_file.readline())
# alternatives = []
# header = list(map(lambda x: x.strip(), input_file.readline().split(' ')))
#
# for i in range(alternatives_count):
#     line = list(map(lambda x: x.strip(), input_file.readline().split(' ')))
#     alternative = {}
#     alternative['name'] = line[0]
#     profitability = 0
#     for c in range(criterias_count):
#         val = float(line[c + 1])
#         if criterias[c]['inverted']:
#             val = 1 / val
#         alternative[header[c + 1]] = val
#         profitability += criterias[c]['function'].get_value(val)
#     alternative['profitability'] = profitability
#     alternatives.append(alternative)
#
# pp.pprint(criterias)
# pp.pprint(alternatives)
#
# pp.pprint(max(alternatives, key=itemgetter('profitability')))

