#include "CashHandler.h"

// Добавление клиенту наличных
int CashHandler::depositCash(map<int, int> banknotes) {
    return this->recordDeposit(banknotes);
}

// Клиент отдаёт наличные
map<int, int> CashHandler::withdrawCash(int moneyAmount) {
    map<int, int> cash = this->recordWithdraw(moneyAmount);

    // проверить что поместится в валидатор
    if (this->countBanknotes(cash) > this->maxDispensableBanknotesAmount) {
        this->recordDeposit(cash);
        return {};
    }

    return cash;
}