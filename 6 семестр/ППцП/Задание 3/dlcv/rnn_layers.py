from __future__ import print_function, division
from builtins import range
import numpy as np

"""
Этот файл определяет типы слоев, которые обычно используются в рекуррентных
нейронных сетях
"""


def rnn_step_forward(x, prev_h, Wx, Wh, b):
    """
    Выполняет прямое распространение для одного временного шага обычной RNN, которая использует
    функцию активации tanh

    Размерность входных данных - D, размерность скрытого состояния - H, размерность миниблока -N 

    Входы:
    - x: Входные данные для текущего временного шага, форма (N, D).
    - prev_h: Скрытое состояние предыдущего временного шага, форма (N, H)
    - Wx: Матрица весов для связей вход-скрытое_состояние, форма (D, H)
    - Wh: Матрица весов для связей скрытое_состояние-скрытое_состояние, форма (H, H)
    - b: Смещения, форма (H,)

    Возвращает кортеж из:
    - next_h: Следующее скрытое состояние, форма (N, H)
    - cache: Кэш значений, необходимых для обратного распространения.
    """

    next_h, cache = None, None

    ##############################################################################
    # Задание: Реализуйте один прямой шаг для обычной RNN. Сохраните следующее   #
    # скрытое состояние и любые значения, которые нужны для обратного рапспро-   #
    # странения в next_h и переменной cache, соответственно                      #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    x_Wx = x.dot(Wx)
    prev_Wh = prev_h.dot(Wh)

    out = x_Wx + prev_Wh + b
    next_h = np.tanh(out)
    cache = (x, Wx, Wh, prev_h, out)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return next_h, cache


def rnn_step_backward(dnext_h, cache):
    """
    Выполняет обратное распространение для одного шага обычной RNN

    Входы:
    - dnext_h: Градиент потерь по next_h, форма (N, H)
    - cache: Кэш с данными прямого прохода
 
    Возвращает кортеж:
    - dx: Градиент по входным данным, форма (N, D)
    - dprev_h: Градиент по предыдущему скрытому состоянию, форма (N, H)
    - dWx: Градиент по весам вход-скрытое состояние, форма (D, H)
    - dWh: Градиент по весам скрытое_состояние-скрытое_состояние, форма (H, H)
    - db: Градиент вектора смещения, форма (H,)
    """

    dx, dprev_h, dWx, dWh, db = None, None, None, None, None

    ##############################################################################
    # ЗАДАНИЕ: Реализуйте обратное распространение для одного шага обычной RNN   #
    #                                                                            #
    # Подсказка: Для функции tanh следует использовать локальную производную,    #
    # выражаемую через значение  tanh.                                           #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    Wx, Wh, b, x, prev_h, next_h = cache
    dtanh = (1 - np.square(next_h)) * dnext_h

    db = np.sum(dtanh, axis=0)
    dWh = np.dot(prev_h.T, dtanh)
    dprev_h = np.dot(dtanh, Wh.T)
    dWx = np.dot(x.T, dtanh)
    dx = np.dot(dtanh, Wx.T)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return dx, dprev_h, dWx, dWh, db


def rnn_forward(x, h0, Wx, Wh, b):
    """
    Выполняет прямое распространение всей последовательности данных через RNN. Входная
    последовательность состоит из T векторов, каждый размерностью D. Скрытое
    состояние RNN имеет размерность H. Мини-блок содержит N последовательностей.
    Функция возвращает скрытые состояния для всех шагов во времени. 

    Входы:
    - x: Входные данные всего временного ряда, форма (N, T, D).
    - h0: Начальное значение скрытого состояния, форма (N, H)
    - Wx: Матрица весов для связей вход-скрытое_состояние, форма (D, H)
    - Wh: Матрица весов для связей скрытое_состояние-скрытое_состояние, форма (H, H)
    - b: Смещения, форма (H,)
    
    Возвращает кортеж из:
    - h: Скрытое состояние для всего временного ряда, форма (N, T, H).
    - cache: Кортеж значений, необходимых для обратного рапространения.
    """

    h, cache = None, None

    ##############################################################################
    # ЗАДАНИЕ: Реализовать прямое распространение для обычной RNN, выполняемое   #
    # на всей последовательности входных данных.Необходимо использовать функцию  #
    # rnn_step_forward, определенную выше.                                       #
    # Вам следует применить цикл for для реализации прямого распространения      #
    ########### ##################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    N, T, D = x.shape
    N, H = h0.shape

    h = np.zeros([N, T, H])
    cache = []

    prev_h = h0

    for t_step in range(T):
        cur_x = x[:, t_step, :]
        prev_h, cache_temp = rnn_step_forward(cur_x, prev_h, Wx, Wh, b)
        h[:, t_step, :] = prev_h
        cache.append(cache_temp)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return h, cache


def rnn_backward(dh, cache):
    """
    Выполняет обратное распространение для обычной RNN с учетом всей последовательности данных

    Входы:
    - dh: Восходящие градиенты для всех скрытых состояний, форма (N, T, H). 
    
    
    Возвращает кортеж:
    - dx: Градиент по входным данным, форма (N, T, D)
    - dh0: Градиент по начальному состоянию, форма (N, H)
    - dWx: Градиент по весам вход-скрытое состояние, форма (D, H)
    - dWh: Градиент по весам скрытое_состояние-скрытое_состояние, форма (H, H)
    - db: Градиент вектора смещения, форма (H,)
    """

    dx, dh0, dWx, dWh, db = None, None, None, None, None

    ##############################################################################
    # ЗАДАНИЕ: Реализовать обратное распространение для обычной RNN, выполняемое #
    # на всей последовательности входных данных. Необходимо использовать функцию #
    # rnn_step_backward, которая определена выше. Для выполнения обратного       #
    # распространения можно использовать цикл for                                #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    # Определяем значения  размерностей
    N, T, H = dh.shape

    # 1ый шаг обратного распространения
    dxl, dprev_h, dWx, dWh, db = rnn_step_backward(dh[:,T-1,:], cache[T-1])

    # Определяем размерность D вектора данных
    _, D = dxl.shape

    # Выделяем память для тензора градиентов по входу x
    dx = np.zeros((N,T,D))

    # Запоминаем градиент dxl  (N,D) для вектора T-1 в тензоре dx 
    dx[:,T-1,:] = dxl

    # Итерации по времени  в обратном порядке, начиная с T-2
    for i in range(T-2, -1, -1):
        # Выполняем шаг обратного распространения
        # dh[:,i,:]+dprev_h  - накопление градиентов между шагами во времени
        dxi, dprev_hi, dWxi, dWhi, dbi = rnn_step_backward(dh[:,i,:]+dprev_h, cache[i])

        # Сохраняем градиент по входу на шаге i в тензоре dx
        dx[:,i,:] = dxi

        # Перезапоминаем градиент по предыдущему скр.состоянию
        dprev_h = dprev_hi

        # Суммируем градиенты по Wxi , Whi, dbi , возникающие 
        # на каждой итерации, и формируем полные  тензоры градиентов
        dWx += dWxi
        dWh += dWhi
        db += dbi

    # Градиент по скр. начальному состоянию h0
    dh0 = dprev_h

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return dx, dh0, dWx, dWh, db


def word_embedding_forward(x, W):
    """
    Прямое распространение для слоя, формирующего векторное 
    представление слов.  Использует мини-блок  размерностью N. Каждая 
    последовательность слов имеет длину T. Словарь  содержит V слов, 
    каждое  слово представляется вектором размерности D.

    Входы:
    - x: Целочисленный массив формы (N, T), содержащий номера слов. 
         Каждый элемент  x должен быть в диапазоне от 0 до V.
    - W: Обучаемая матрица векторов слов, форма (V, D).
    Возвращает:
    - out: Массив формы (N, T, D), содержащий вектора слов для всей 
             последовательности номеров входных слов.
    - cache: Кэш значений, необходимых для обратного распространения
    """

    out, cache = None, None

    ##############################################################################
    # ЗАДАНИЕ: Реализовать прямое распространение для вложения слов              #
    #                                                                            #
    # ПОДСКАЗКА: Решение должно быть в виде одной строки,использующей индексацию #
    # NumPy массивов.                                                            #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    out = W[x]
    cache = (x, W)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return out, cache


def word_embedding_backward(dout, cache):
    """
    Обратное распространение для слоя встраивания слов. Нельзя 
    выполнять обратное  распространение на уровне слов, так как они  
    являются целыми числами, поэтому градиент возвращается только для
    матрицы векторов слов.
        
    Входы:
    - dout: Восходящий поток градиентов формы (N, T, D)
    - cache: Кэш значений прямого распространения
    Возвращает:
    - dW: Градиент матрицы векторов слов, форма (V, D).
    """

    dW = None

    ##############################################################################
    # ЗАДАНИЕ: Реализуйте обратное распространение для встраивания слов          #
    #                                                                            #
    # Обратите внимание, что слова могут появляться более одного раза в          #
    # последовательности.                                                        #
    # ПОДСКАЗКА: Воспользуйтесь функцией np.add.at                               #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    x, W = cache             # x целочисл. массив формы (N,T)
    dW = np.zeros(W.shape)   # dW -> (V,D)
   
    # np.add.at  выполняет:
    # для всех row in range(N)
    #           для всех col in range(T)
    #                  dW[ x[row,col] , :] += dout[row,col, :] 
    # т.е. добавляет  восх. градиент к градиенту соответствующего вектора слова
    np.add.at(dW, x, dout)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return dW


def sigmoid(x):
    """
    Численно стабильная версия логистической сигмоидальной функции.
    """

    pos_mask = (x >= 0)
    neg_mask = (x < 0)
    z = np.zeros_like(x)
    z[pos_mask] = np.exp(-x[pos_mask])
    z[neg_mask] = np.exp(x[neg_mask])
    top = np.ones_like(x)
    top[neg_mask] = z[neg_mask]

    return top / (1 + z)


def lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b):
    """
    Прямое распространение для одного шага по времени LSTM.

    N - размер миниблока
    
    - x: Входные данные на одном временном шаге, форма (N, D).
    - prev_h: Пред. скрытое состояние, форма (N, H)
    - prev_c: Пред. cостояние ячейки LSTM, форма (N, H)
    - Wx: Матрица весов  вход-скр_сост, форма (D, 4H)
    - Wh: Матрица весов  скр_сост-скр_сост, форма (H, 4H)
    - b: Смещения, форма (4H,)
    - next_h: Следующее скрытое состояние, форма (N, H)
    - next_c: След. cостояние ячейки LSTM, форма (N, H)
    - cache: Кэш значений для обратного распространения.
    """

    next_h, next_c, cache = None, None, None

    ##############################################################################
    # Задание: Реализуйте один прямой временной шаг для LSTM. Используйте        #
    # численно стабильную версию сингмоидальной функции, определенную выше       #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    N, H = prev_h.shape
    a = np.dot(x, Wx) + np.dot(prev_h, Wh) + b  # (1)
    i = sigmoid(a[:, 0:H])  # (2-5)
    f = sigmoid(a[:, H:2 * H])
    o = sigmoid(a[:, 2 * H:3 * H])
    g = np.tanh(a[:, 3 * H:4 * H])
    next_c = f * prev_c + i * g  # (6)
    next_h = o * np.tanh(next_c)  # (7)

    cache = (next_c, i, f, o, g, x, prev_h, prev_c, Wh, Wx)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return next_h, next_c, cache


def lstm_step_backward(dnext_h, dnext_c, cache):
    """
    Выполняет обратное распространение для одного шага LSTM

    Входы:
    - dnext_h: Градиент потерь по next_h, форма (N, H)
    - dnext_c: Градиент по next_c, форма (N, H)
    - cache: Кэш с данными прямого прохода
 
    Возвращает кортеж:
    - dx: Градиент по входным данным, форма (N, D)
    - dprev_h: Градиент по предыдущему скрытому состоянию, форма (N, H)
    - dprev_c: Градиент по prev_c, форма(N, H)
    - dWx: Градиент по весам вход-скрытое состояние, форма (D, 4H)
    - dWh: Градиент по весам скрытое_состояние-скрытое_состояние, форма (H, 4H)
    - db: Градиент вектора смещения, форма (4H,)
    """

    dx, dprev_h, dprev_c, dWx, dWh, db = None, None, None, None, None, None

    ##############################################################################
    # ЗАДАНИЕ: Реализуйте обратное распространение для одного шага LSTM          #
    #                                                                            #
    # Подсказка: Для функции tanh следует использовать локальную производную,    #
    # выражаемую через значение  tanh.                                           #
    ##############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    
    # Извлекаем значения из кэша
    next_c, i, f, o, g, x, prev_h, prev_c, Wh, Wx = cache
    
    # Градиент по “o” выражения next_h = o*np.tanh(next_c) 
    # Восх. градиент (dnext_h) *  лок. градиент =(tanh(next_c))
    do = dnext_h*np.tanh(next_c) # (N,H)*(N,H) ->(N,H)
    
    # Градиент по prev_c  равен  (см. схему LSTM):
    # {dnext_c +  лок.градиент  (tanh(next_c))*(восх.град.(tanh)= dnext_h*o)}*f
    dprev_c = (dnext_c + dnext_h * o * (1 - np.tanh(next_c) ** 2)) * f # (N,H)
    
    # Градиент по f  равен  (см. схему LSTM):
    # {dnext_c)+лок.градиент  (tanh(next_c))*(восх.град.(tanh)= dnext_h*o)}* prev_c
    df = (dnext_c + dnext_h * o * (1 - np.tanh(next_c) ** 2)) * prev_c # (N,H)
    
    # Градиенты по i и g аналогично  (см. схему LSTM):
    di = g * (dnext_c + dnext_h * o * (1 - np.tanh(next_c) ** 2)) # (N,H)
    dg = i * (dnext_c + dnext_h * o * (1 - np.tanh(next_c) ** 2)) # (N,H)

    # Градиенты по составляющим общей активности ”a” 
    dai = i * (1 - i) * di    # (N,H)
    daf = f * (1 - f) * df    # (N,H)
    dao = o * (1 - o) * do    # (N,H)
    dag = (1 - g ** 2) * dg   # (N,H)

    # Градиент по общей активности ”a”
    da = np.concatenate((dai, daf, dao, dag), axis=1)  # (N,4H)
    
    # Градиент по x выражения a = x.dot(Wx) + prev_h.dot(Wh) + b 
    # (a)’->(восх градиент ,т.е. da) dot  Wx.T
    dx = da.dot(Wx.T)    # (N,4H)*(D,4H)’ ->(N,D)

    # Градиент по prev_h выражения a = x.dot(Wx) + prev_h.dot(Wh) + b 
    # (a)’-> (восх градиент ,т.е. da) dot  Wh.T
    dprev_h = da.dot(Wh.T) # (N,4H)*(H,4H)’ ->(N,H)

    # Градиент по Wx выражения a = x.dot(Wx) + prev_h.dot(Wh) + b 
    # (a )’-> x.T dot (восх градиент ,т.е. da)
    dWx = x.T.dot(da) # (N,D)’*(N,4H) ->(D,4H)

    # Градиент по Wh выражения a = x.dot(Wx) + prev_h.dot(Wh) + b 
    # (a)’-> prev_h.T dot (восх градиент ,т.е. da)
    dWh = prev_h.T.dot(da) # (N,H)’*(N,4H) ->(H,4H)

    # Градиент потерь по  смещениям
    db = np.sum(da, axis = 0) # (N,4H) ->(4H,)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return dx, dprev_h, dprev_c, dWx, dWh, db


def lstm_forward(x, h0, Wx, Wh, b):
    """
    Прямое распространение всей последовательности данных
    через LSTM. Входная последовательность x состоит из T векторов,
    каждый размерностью D. Функция возвращает скрытые состояния 
    для всех шагов во времени. 
    Обратите внимание, что начальное состояние ячейки передается как 
    входное значение,  которое   равно нулю. Также обратите внимание,
    что состояние ячейки не возвращается; это внутренняя переменная LSTM
    и она не доступна извне.
  
    Входы:
    - x: Входные данные всего временного ряда, форма (N, T, D).
    - h0: Начальное значение скрытого состояния, форма (N, H)
    - Wx: Матрица весов вход-скрытое_состояние, форма (D, 4H)
    - Wh: Матрица весов скр_сост-скр_сост, форма (H, 4H)
    - b: Смещения, форма (4H,)

     Выход – кортеж из:
     - h: Скрытые состояния  для всех шагов во времени, форма (N, T, H)
     - cache: Значения, необходимые для вычислений на обратном пути.
    """

    h, cache = None, None
    
    #############################################################################
    #Задание:Реализовать прямое распространение для LSTM всего временного ряда  #
    #Необходимо использовать функцию lstm_step_forward , определенную выше      #
    #############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****

    T = x.shape[1]
    prev_h = h0
    prev_c = np.zeros_like(h0)
    h, cache = [], []
    for t in range(T):
        next_h, next_c, step_cache = lstm_step_forward(x[:, t, :], prev_h, prev_c, Wx, Wh, b)
        cache.append(step_cache)
        h.append(next_h)
        prev_h, prev_c = next_h, next_c
    h = np.array(h).transpose(1, 0, 2)

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return h, cache


def lstm_backward(dh, cache):
    """
    Выполняет обратное распространение для LSTM с учетом 
    всей последовательности данных.
    Входы:
    - dh: Восходящие градиенты по всем скрытым состояниям,(N, T, H). 
    - cache: Значения запомненные при прямом распространении
    Возвращает кортеж:
    - dx: Градиент по входным данным, форма (N, T, D)
    - dh0: Градиент по начальному состоянию, форма (N, H)
    - dWx: Градиент по весам вход-скр_сост, форма (D, 4H)
    - dWh: Градиент по весам скр_сост-скр_сост, форма (H, 4H)
    - db: Градиент по смещениям, форма (4H,)
    """

    dx, dh0, dWx, dWh, db = None, None, None, None, None

    #############################################################################
    # Задание:Реализовать обратное распространение в LSTM всего временного ряда #
    # Необходимо использовать функцию lstm_step_backward, определенную выше.    #
    #############################################################################
    # *****НАЧАЛО ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    
    # Определяем значения  размерностей
    N, T, H = dh.shape

    # 1ый шаг обратного распространения
    dxl, dprev_h, dprev_c, dWx, dWh, db = lstm_step_backward(dh[:,T-1,:], np.zeros_like(dh[:,T-1,:]), cache[T-1])
    
    # Определяем размерность D вектора данных
    _, D = dxl.shape

    # Выделяем память для тензора градиентов по входу x
    dx = np.zeros((N,T,D))

     # Запоминаем градиент dxl  (N,D) для вектора T-1 в тензоре dx 
    dx[:,T-1,:] = dxl

    # Итерации по времени  в обратном порядке, начиная с T-2 (BPTT)
    for i in range(T-2, -1, -1):
        dxi, dprev_h, dprev_c, dWxi, dWhi, dbi = lstm_step_backward(dh[:,i,:] + dprev_h, dprev_c, cache[i])

        # Сохраняем градиент по входу на шаге i в тензоре dx
        dx[:,i,:] = dxi

        # Суммируем градиенты по Wxi , Whi, dbi , возникающие 
        # на каждой итерации, и формируем полные  тензоры градиентов
        dWx += dWxi
        dWh += dWhi
        db += dbi

    # Градиент по скр. начальному состоянию h0
    dh0 = dprev_h

    # *****КОНЕЦ ВАШЕГО КОДА (НЕ УДАЛЯЙТЕ/НЕ МОДИФИЦИРУЙТЕ ЭТУ СТРОКУ)*****
    ##############################################################################
    #                               Конец Вашего кода                            #
    ##############################################################################

    return dx, dh0, dWx, dWh, db


def temporal_affine_forward(x, w, b):
    """
    Функция прямого распространения для временного афинного слоя. Вход представлен векторами
    длиной D, которые собраны в мини-блоки из N временных рядов каждый длиной T. Функция
    используется для преобразования этих векторов в новые векторы длиной M. 
    

    Входы:
    - x: Входные данные, форма (N, T, D)
    - w: Веса, форма (D, M)
    - b: Смещения, форма (M,)

    Фозвращает кортех из:
    - out: Выходные данные формы (N, T, M)
    - cache: Значения, необходимые для обратного распространения
    """

    N, T, D = x.shape
    M = b.shape[0]

    # реформатируем входные данные в массив размером (N*T,D), умножаем на матрицу весов размером (D,M),
    # получаем массив формы (N*T,M) и реформатируем его в массив формы (N,T,M)
    out = x.reshape(N * T, D).dot(w).reshape(N, T, M) + b
    cache = x, w, b, out

    return out, cache


def temporal_affine_backward(dout, cache):
    """
    Обратное распространение через афинный слой

    Вход:
    - dout: Восходящие градиенты формы (N, T, M)
    - cache: Значения, запомненные при прямом распростарнении 

    Возворащаетк кортеж из
    - dx: Градиент по входу, форма (N, T, D)
    - dw: Градиент по весам, форма (D, M)
    - db: Градиент по смещениям, форма (M,)
    """

    x, w, b, out = cache
    N, T, D = x.shape
    M = b.shape[0]

    # Если out=x*w+b, то dx=dout*w.T
    dx = dout.reshape(N * T, M).dot(w.T).reshape(N, T, D)

    # Если out=x*w+b, то dx=x.T*dout или dx=dout.T*x.T 
    dw = dout.reshape(N * T, M).T.dot(x.reshape(N * T, D)).T
    
    # Если out=x*w+b, то db=1*восх.градиент
    db = dout.sum(axis=(0, 1))

    return dx, dw, db


def temporal_softmax_loss(x, y, mask, verbose=False):
    """
    Временная версия softmax loss для использования в RNN. Мы предполагаем, что мы 
    делаем предсказания по словарю размера V для каждого элемента временного ряда 
    длины T по мини-блоку размера N. Входные данные x дают рейтинги для всех элементов
    словаря на каждом временном шаге, а y дает индексы истинных элементов на каждом
    временном шаге. Мы используем кросс-энтропийные потери на каждом временном шаге, 
    суммируя потери по всем временным шагам и усредняя по мини-блоку.

    Мы можем игнорировать выходные данные модели на некоторых временных шагах, 
    поскольку в мини-блок могли быть объединены последовательности разной длины
    и дополнены NULL-токенами для выравнивания длины. Необязательный аргумент mask
    сообщает нам, какие элементы должны учитываться при вычислении потерь.

    Входы:
    - x: Входные рейтинги, форма (N, T, V)
    - y: Корректные индексы, форма (N, T), где каждый элемент принадлежит диапазону
         0 <= y[i, t] < V
    - mask: Логический массив формы (N, T), где mask[i, t] сообщает, действительно ли 
      рейтинг x[i, t] должен быть учтен при вычислении loss.

    Возвращает кортеж из:
    - loss: Скаляр, представляющий потери
    - dx: Градиент потерь (loss) по отнощению к рейтингам x.
    """

    N, T, V = x.shape

    x_flat = x.reshape(N * T, V)
    y_flat = y.reshape(N * T)
    mask_flat = mask.reshape(N * T)

    probs = np.exp(x_flat - np.max(x_flat, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)
    loss = -np.sum(mask_flat * np.log(probs[np.arange(N * T), y_flat])) / N
    dx_flat = probs.copy()
    dx_flat[np.arange(N * T), y_flat] -= 1
    dx_flat /= N
    dx_flat *= mask_flat[:, None]

    if verbose: print('dx_flat: ', dx_flat.shape)

    dx = dx_flat.reshape(N, T, V)

    return loss, dx
