#pragma once

class BillAcceptor
{
public:
    //BillAcceptor();

    void putCash(int cash, int bills);
    void getbackCash();
    void getCash(int cash);

protected:
    int cash;
    int banknotes;

    void checkBanknotes();

    void setSum();
};

