#pragma once

class BillAcceptor
{
public:
    void putCash(int cash, int bills);
    void getbackCash();
    void getCash(int cash);

protected:
    int cash = 0;
    int banknotes = 0;

    void checkBanknotes();

    void setSum();
};

