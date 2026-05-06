#pragma once

#include <map> 
using namespace std;

class BillAcceptor
{
public:
    BillAcceptor() {};
    map<int, int>* cash = NULL;

    int getCash(map<int, int>* cash);
    void returnCash();
    void takeCashInHandler();

    int calculateCash();    // Подсчитать внесённую наличку
    int countBanknotes();   // Подсчитать число банкнот

protected:
    static const int max_banknotes = 8000;  // Максимальное число банкнот за раз

    bool validateBanknotes();   // Проверка что банкноты нормальные
};

