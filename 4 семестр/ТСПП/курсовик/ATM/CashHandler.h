#pragma once

#include <map>
#include <vector>
using namespace std;

class CashHandler
{
public:
    CashHandler() {};

    bool canAcceptBanknotes(int banknotesAmount);   // проверка на вместимость
    bool canDispenseAmount(int moneyAmount);        // проверка наличия нала для выдачи

    bool cashIn(map<int, int> bills, int amount);
    map<int, int> cashOut(int amount);

protected:
    const vector<int> denominations = { 5000, 2000, 1000, 500, 200, 100, 50 };
    const int max_banknotes = 8000;   // максимальная вместимость купюр

    map<int, int> bills = {};   // набор купюр разного номинала
    int bills_amount = 0;       // число купюр

    //int maxGivableBanknotesAmount = 50; // НУЖНО КАК-ТО СЧИТАТЬ С BILL_ACCEPTOR
};

