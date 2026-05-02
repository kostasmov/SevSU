#pragma once

class CashHandler
{
public:
    CashHandler() {};

    bool canAcceptBanknotes(int count); // проверка на вместимость
    //void cashIn(int sum, int bills);
    //void cashOut(int sum);

protected:
    int banknotes = 0;      // число купюр
    const int max_banknotes = 10; // максимальная вместимость купюр
};

