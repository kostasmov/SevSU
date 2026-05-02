#pragma once

#include <map>
#include <iostream>
using namespace std;

class CashHandler
{
public:
    CashHandler() {};

    bool canAcceptBanknotes(int count); // проверка на вместимость

    bool cashIn(map<int, int>* bills, int amount);
    //void cashOut() { cout << bills[500] << endl; };

protected:
    const int max_banknotes = 10;   // максимальная вместимость купюр

    map<int, int> bills = {};   // набор купюр разного номинала
    int bills_amount = 0;       // число купюр
};

