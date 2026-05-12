#pragma once

#include "CashHolder.h"

using namespace std;

class CashHandler :
    public CashHolder
{
public:
    CashHandler() : CashHolder(8000) {
        //this->cash = {
        //    {50, 10},
        //    {100, 20},  
        //    {500, 15},
        //    {1000, 5},
        //    {2000, 5}
        //};
    }

    int depositCash(map<int, int> banknotes) override;      // добавить наличные
    map<int, int> withdrawCash(int moneyAmount) override;   // отдать наличные

protected:
    int maxDispensableBanknotesAmount = 50; // НУЖНО КАК-ТО СЧИТАТЬ С BILL_ACCEPTOR
};

