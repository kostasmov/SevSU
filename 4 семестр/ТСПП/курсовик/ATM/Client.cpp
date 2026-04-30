#include "Client.h"

// добавить новую карту в "кошелёк" пользователя
void Client::addCard(BankCard* card) {
	this->cards.push_back(card);
}

// доступ к набору банковских карт
vector<BankCard*> Client::getCards() {
	return this->cards;
}