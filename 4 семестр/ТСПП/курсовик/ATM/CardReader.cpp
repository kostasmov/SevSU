#include <iostream>

#include "CardReader.h"
#include "BankCard.h"

bool CardReader::getCard(BankCard* card) {
	/* Ридер принимает карту
	* для удобства все карты по умолчанию корректны
	* но если карта уже есть в ридере - отказ */

	if (this->isCardPresent()) return 0;
	
	this->card = card;
	return 1;
}

bool CardReader::returnCard() {
	/* Ридер возвращает карту
	* но только если она вообще в нём есть */

	if (not this->isCardPresent()) return 0;

	this->card = NULL;
	return 1;
}

// проверка наличия карты в ридере
bool CardReader::isCardPresent() const {
	return (this->card ? true : false);
}

//// вывод информации о карте
//void CardReader::getCardInfo() {
//	// НЕ РАБОТАЕТ - ОБРАЩАТЬСЯ НАПРЯМУЮ К cardReader.card
//}