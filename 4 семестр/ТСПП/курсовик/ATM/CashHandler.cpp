#include "CashHandler.h"

// Проверить, помещается ли в банкомат указанное число купюр
bool CashHandler::canAcceptBanknotes(int count) {
	if (this->bills_amount + count > this->max_banknotes)
		return 0;

	return 1;
}

// Проверить, может ли банкомат выдать требуемую сумму
bool CashHandler::canDispenseAmount(int amount) {
    if (amount <= 0 || amount % 50 != 0) {
        return false;
    }

    int remaining = amount;

    // проверяем от больших номиналов к меньшим - сколько купюр можем выдать
    for (int d : denominations) {
        int need = remaining / d;
        int canGive = min(need, bills[d]);
        remaining -= canGive * d;
    }

    return remaining == 0;
}


// Внесение в кассу новых купюр
bool CashHandler::cashIn(map<int, int>* bills, int amount) {
	if (!canAcceptBanknotes(amount)) return 0;

	for (const auto& [key, value] : *bills) {
		this->bills[key] += value;
	}

	this->bills_amount += amount;

	return 1;
}

/*void CashHandler::cashOut(int sum) {

}*/

//void CashHandler::sendAlert() {
//
//}