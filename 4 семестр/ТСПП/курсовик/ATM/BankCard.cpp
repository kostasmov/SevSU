#include "BankCard.h"

BankCard::BankCard(int n, string bank, Client* owner, int PIN) {
	this->number = n;
	this->bank = bank;
	this->owner = owner;
	this->isBlocked = false;
	this->PIN = PIN;
}

bool BankCard::getBlockState() {
	return this->isBlocked;
}

int BankCard::getNumber() {
	return this->number;
}

string BankCard::getBank() {
	return this->bank;
}

/*void BankCard::checkPIN() {

}*/

/*void BankCard::setBlockState(void state) {

}*/