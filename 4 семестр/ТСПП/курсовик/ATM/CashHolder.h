#pragma once

#include <map>
#include <vector>

using namespace std;

// ИНТЕРФЕЙС ДЛЯ СУЩНОСТЕЙ КОТОРЫЕ МОГУТ ИМЕТЬ И ИСПОЛЬЗОВАТЬ НАЛИЧНЫЕ

class CashHolder {
public:
    CashHolder(int maxBanknotes = INF) { this->max_banknotes = maxBanknotes; }
    ~CashHolder() = default;

    map<int, int> getCashInfo() { return this->cash; };

    // -----------------
    virtual int depositCash(map<int, int> banknotes) = 0;       // добавить купюры
    virtual map<int, int> withdrawCash(int moneyAmount) = 0;    // изъять купюры на сумму
    // -----------------

    bool canAccept(int banknotesCount);
    bool canDispense(int moneyAmount);
    
    int calculateCash();
    static int calculateCash(map<int, int> banknotes);

    int countBanknotes();
    static int countBanknotes(map<int, int> banknotes);

    int countFreeSlots();

protected:
    static const int INF = 1000000000;
    static const vector<int> denominations; // номиналы купюр

    int max_banknotes;  // ограничение на переносимое число банкнот

    map<int, int> cash = {};

    // Внутренняя реализация Deposit (внесение)
    bool recordDeposit(map<int, int> bills);

    // Внутренняя реализация Withdraw (выдача)
    map<int, int> recordWithdraw(int moneyAmount);
};