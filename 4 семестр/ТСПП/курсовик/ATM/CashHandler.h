#pragma once

class CashHandler
{
public:
    CashHandler() {};

    void cashIn(int sum, int bills);
    void cashOut(int sum);

protected:
    int cash = 0;       // сумма наличных

    int banknotes = 0;  // число купюр
    int maxBanknotes;   // максимальное число купюр

    // подсчёт купюр разного номинала
    int cash100;        
    int cash500;
    int cash1000;
    int cash5000;
    
    void sendAlert();
};

