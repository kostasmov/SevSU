#include "Client.h"

void Client::addCard(BankCard* card) {
	this->cards.push_back(card);
}

vector<BankCard*> Client::getCards() {
	return this->cards;
}