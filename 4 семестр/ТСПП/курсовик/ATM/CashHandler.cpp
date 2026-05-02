#include "CashHandler.h"

// Проверить помещается ли в банкомат указанное число купюр
bool CashHandler::canAcceptBanknotes(int count) {
	if (this->bills_amount + count > this->max_banknotes)
		return 0;

	return 1;
}

// Внесение в кассу новых купюр
bool CashHandler::cashIn(map<int, int>* bills, int amount) {
	if (!bills) return 0;
	if (!canAcceptBanknotes(amount)) return 0;

	for (const auto& [key, value] : *bills) {
		this->bills[key] += value;
	}

	return 1;
}

//void CashHandler::cashOut(int sum) {
//
//}
//
//void CashHandler::sendAlert() {
//
//}