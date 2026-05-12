#include "BillAcceptor.h"

/* Внесение купюр в банкомат
* 404 - банкнот слишком много
* 405 - ошибка валидации
* 1 - операция прошла успешно
*/
int BillAcceptor::depositCash(map<int, int> banknotes) {
    this->cash = banknotes;

    if (this->countBanknotes() > this->max_banknotes) {
        this->withdrawCash();
        return 404;
    }

    if (!validateBanknotes()) {
        this->withdrawCash();
        return 405;
    }

    return 1;
}

// Отдать ВСЕ хранимые наличные
map<int, int> BillAcceptor::withdrawCash(int n) {
    map<int, int> cash = this->cash;
    this->cash = {};

    return cash;
}


// Передача наличных в кассу
bool BillAcceptor::takeCashInHandler(CashHandler& handler) {
    if (!handler.depositCash(this->cash)) return false;

    this->cash = {};
    return true;
}


// Проверить корректность купюр
bool BillAcceptor::validateBanknotes() {
    if (this->cash.empty()) return 0;

	// По умолчанию все банкноты корректные - не мятые, не подделанные
	return true;
}


