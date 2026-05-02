#include "CashHandler.h"

// Проверить помещается ли в банкомат указанное число купюр
bool CashHandler::canAcceptBanknotes(int count) {
	if (this->banknotes + count > this->max_banknotes)
		return 0;

	return 1;
}

//void CashHandler::cashIn(int sum, int bills) {
//
//}
//
//void CashHandler::cashOut(int sum) {
//
//}
//
//void CashHandler::sendAlert() {
//
//}