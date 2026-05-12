#include "CashHolder.h"

// Номиналы купюр
const vector<int> CashHolder::denominations = { 5000, 1000, 500, 100, 50 };


// Пополнение наличных
bool CashHolder::recordDeposit(map<int, int> cash) {
    if (!this->canAccept(this->countBanknotes(cash))) return false;

    for (auto [denomination, count] : cash) {
		this->cash[denomination] += count;
	}

    return true;
}


// Изъятие наличных
map<int, int> CashHolder::recordWithdraw(int moneyAmount) {
    if (!this->canDispense(moneyAmount)) return {};

    map<int, int> withdrawCash;
    int remaining = moneyAmount;

    for (int d : denominations) {
        int need = remaining / d;
        int canGive = min(need, this->cash[d]);

        remaining -= d * canGive;
        this->cash[d] -= canGive;

        withdrawCash[d] = canGive;
    }

    return withdrawCash;
}


// Проверить, можно ли принять ещё n купюр
bool CashHolder::canAccept(int banknotesCount) {
    if (this->countBanknotes() + banknotesCount > this->max_banknotes)
        return false;

    return true;
}


// Проверить, можно ли выдать требуемую сумму
bool CashHolder::canDispense(int moneyAmount) {
    if (moneyAmount <= 0 || moneyAmount % 50 != 0) {
        return false;
    }

    int remaining = moneyAmount;

    // проверяем от больших номиналов к меньшим - сколько купюр можем выдать
    for (int d : this->denominations) {
        int need = remaining / d;
        int canGive = min(need, this->cash[d]);
        remaining -= canGive * d;
    }

    return (remaining == 0);
}


// Подсчитать сумму наличных
int CashHolder::calculateCash() {
    return this->calculateCash(this->cash);
}
int CashHolder::calculateCash(map<int, int> banknotes) {
    int total = 0;

    for (auto [denomination, count] : banknotes) {
        total += denomination * count;
    }

    return total;
}


// Подсчитать число купюр
int CashHolder::countBanknotes() {
    return CashHolder::countBanknotes(this->cash);
}
int CashHolder::countBanknotes(map<int, int> banknotes) {
    int amount = 0;

    for (auto [denomination, count] : banknotes) {
        amount += count;
    }

    return amount;
}