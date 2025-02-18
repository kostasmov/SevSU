# shopSmart.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Это предполагаемый результат этого скрипта после его заполнения:   

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""
from __future__ import print_function
import shop


def shopSmart(orderList, fruitShops):
    """
    Возвращает магазин с минимальной стоимостью заказа
        orderList: Список-заказ из кортежей (fruit, numPound) 
        fruitShops: Список магазинов типа shop
    """
    minTotalCost = -1
    bestShopName = ''

    for shop in fruitShops:
        totalCost = shop.getPriceOfOrder(orderList)

        if totalCost < minTotalCost or minTotalCost < 0:
            minTotalCost = totalCost
            bestShopName = shop.getName()

    print(f"For orders: {orderList} best shop is {bestShopName}")
    return f"<FruitShop: {bestShopName}>"


if __name__ == '__main__':
    "Этот код выполняется, когда Вы запускаете скрипт из командной строки"
    orders = [('apples', 1.0), ('oranges', 3.0)]
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    shop1 = shop.FruitShop('shop1', dir1)
    dir2 = {'apples': 1.0, 'oranges': 5.0}
    shop2 = shop.FruitShop('shop2', dir2)
    shops = [shop1, shop2]
    print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
    orders = [('apples', 3.0)]
    print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
