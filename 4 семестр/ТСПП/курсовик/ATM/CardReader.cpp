#include <iostream>

#include "CardReader.h"
#include "BankCard.h"

bool CardReader::setCard(BankCard* card) {
	if (not this->isCardPresent()) {
		this->card = card;
		return 1;
	}
	else return 0;
}

bool CardReader::getbackCard() {
	if (this->isCardPresent()) {
		this->card = NULL;
		return 1;
	}
	else
		return 0;
}

// проверка наличия карты в ридере
bool CardReader::isCardPresent() {
	return (this->card ? true : false);
}

// вывод информации о карте
void CardReader::getCardInfo() {
	cout << "Bank: " << this->card->getBank() << endl;
	cout << "Number: " << this->card->getNumber() << endl;
	cout << "Is card blocked: " << (this->card->getBlockState() ? "YES" : "NO") << endl;
}

/*void CardReader::sendAlert() {

}*/