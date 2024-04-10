from dlcv.layers import *
from dlcv.fast_layers import *


def affine_relu_forward(x, w, b):
    """
    Удобный слой, который выполняет аффинное преобразование и затем применяет ReLU 

    Вход:
    - x: Вход аффинного слоя 
    - w, b: веса и смещение слоя

    Возвращает корьеж из:
    - out: выход ReLU
    - cache: объект, используемый при обратном распростанении
    """

    a, fc_cache = affine_forward(x, w, b)
    out, relu_cache = relu_forward(a)
    cache = (fc_cache, relu_cache)

    return out, cache


def affine_relu_backward(dout, cache):
    """
    Обратное распространение через слой affine-relu
    """

    fc_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = affine_backward(da, fc_cache)

    return dx, dw, db


# слой: fc-->bn-->relu
def affine_batchnorm_relu_forward(x, w, b, gamma, beta, bn_param):
    a_out, a_cache = affine_forward(x, w, b)
    b_out, b_cache = batchnorm_forward(a_out, gamma, beta, bn_param)
    out, r_cache = relu_forward(b_out)
    cache = (a_cache, b_cache, r_cache)

    return out, cache


def affine_batchnorm_relu_backward(dout, cache):
    a_cache, b_cache, r_cache = cache
    dx1 = relu_backward(dout, r_cache)
    dx2, dgamma, dbeta = batchnorm_backward(dx1, b_cache)
    dx, dw, db = affine_backward(dx2, a_cache)
    return dx, dw, db, dgamma, dbeta


def conv_relu_forward(x, w, b, conv_param):
    """
    Удобный слой, который реализует свертку + ReLU

    Входы:
    - x: Вход сверточного слоя
    - w, b, conv_param: Веса и параметры сверточного слоя 

    Возвращает кортеж:
    - out: Выход  ReLU
    - cache: объект, используемый при обратном распространении
    """
    
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    out, relu_cache = relu_forward(a)
    cache = (conv_cache, relu_cache)

    return out, cache


def conv_relu_backward(dout, cache):
    """
    Реализует обратное распротсанение для слоя conv-relu.
    """

    conv_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)

    return dx, dw, db


def conv_bn_relu_forward(x, w, b, gamma, beta, conv_param, bn_param):
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    an, bn_cache = spatial_batchnorm_forward(a, gamma, beta, bn_param)
    out, relu_cache = relu_forward(an)
    cache = (conv_cache, bn_cache, relu_cache)

    return out, cache


def conv_bn_relu_backward(dout, cache):
    conv_cache, bn_cache, relu_cache = cache
    dan = relu_backward(dout, relu_cache)
    da, dgamma, dbeta = spatial_batchnorm_backward(dan, bn_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)

    return dx, dw, db, dgamma, dbeta


def conv_relu_pool_forward(x, w, b, conv_param, pool_param):
    """
    Удобный слой, который выполняет свертку, ReLU и пулинг

    Входы:
    - x: Вход сверточного слоя
    - w, b, conv_param: Веса и парметры сверточного слоя
    - pool_param: Параметры слоя пулинга

    Возвращает кортеж:
    - out: Выход слоя пулинга
    - cache: объект, используемый при обратном распространении
    """

    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    s, relu_cache = relu_forward(a)
    out, pool_cache = max_pool_forward_fast(s, pool_param)
    cache = (conv_cache, relu_cache, pool_cache)

    return out, cache


def conv_relu_pool_backward(dout, cache):
    """
    Реализует обратное рапсространение для слоя conv-relu-pool
    """

    conv_cache, relu_cache, pool_cache = cache
    ds = max_pool_backward_fast(dout, pool_cache)
    da = relu_backward(ds, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)

    return dx, dw, db
