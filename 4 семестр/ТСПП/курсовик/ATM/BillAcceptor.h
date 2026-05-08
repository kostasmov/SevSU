#pragma once

#include <map> 
using namespace std;

class BillAcceptor
{
public:
    BillAcceptor() {};

    const int max_banknotes = 50;  // максимальное число купюр за раз

    map<int, int> cash = {};
    int getCash(map<int, int> cash);

    void returnCash();          // заглушки
    void takeCashInHandler();   

    int calculateCash();    // подсчитать внесённую наличку
    int countBanknotes();   // подсчитать число банкнот

protected:
    bool validateBanknotes();   // Проверка что банкноты нормальные
};

