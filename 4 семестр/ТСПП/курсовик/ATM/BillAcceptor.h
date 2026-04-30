#pragma once

class BillAcceptor
{
public:
    BillAcceptor() {};

    void putCash(int cash, int bills);
    void getbackCash();
    void getCash(int cash);

protected:
    //int cash;
    //int banknotes;

    bool checkBanknotes();  // проверка что банкноты нормальные

    void setSum();
};

