#pragma once

#include "CashHolder.h"
#include "CashHandler.h"

class BillAcceptor :
    public CashHolder
{
public:
    BillAcceptor() : CashHolder(50) {};

    bool takeCashInHandler(CashHandler& handler);

    int depositCash(map<int, int> banknotes) override;  // добавить наличные
    map<int, int> withdrawCash(int n=0) override;       // отдать ВСЕ наличные

protected:
    bool validateBanknotes();   // Проверка что банкноты нормальные
};

