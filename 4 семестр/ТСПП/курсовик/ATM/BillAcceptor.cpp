#include "BillAcceptor.h"

/* Внесение купюр в банкомат
* 404 - банкнот слишком много
* 405 - ошибка валидации
* 1 - операция прошла успешно
*/
int BillAcceptor::getCash(map<int, int>* cash) {
    this->cash = cash;

    if (this->countBanknotes() > this->max_banknotes) {
        returnCash();
        return 404;
    }

    if (!validateBanknotes()) {
        returnCash();
        return 405;
    }

    return 1;
}

void BillAcceptor::returnCash() {
	// заглушка
}

void BillAcceptor::takeCashInHandler() {
    this->cash = NULL;
    // заглушка
}

// Проверить корректность купюр
bool BillAcceptor::validateBanknotes() {
    if (!this->cash) return 0;

	// По умолчанию все банкноты корректные - не мятые, не подделанные
	return true;
}

// Подсчитать сумму 
int BillAcceptor::calculateCash() {
    if (!this->cash) return 0;

    int total = 0;

    for (auto i = this->cash->begin(); i != this->cash->end(); ++i) {
        total += i->first * i->second;
    }

    return total;
}

// Подсчитать число купюр
int BillAcceptor::countBanknotes() {
    if (!this->cash) return 0;

    int amount = 0;

    for (auto i = this->cash->begin(); i != this->cash->end(); ++i) {
        amount += i->second;
    }

    return amount;
}