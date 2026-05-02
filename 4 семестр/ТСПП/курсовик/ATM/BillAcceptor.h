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
    //void takeCashInHandler();

    int calculateCash();    // Подсчитать внесённую наличку

protected:
    const int max_banknotes = 100;  // Максимальное число банкнот за раз

    bool validateBanknotes();   // Проверка что банкноты нормальные
    int countBanknotes();       // Подсчитать число банкнот
};

