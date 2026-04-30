#include "BankCard.h"

BankCard::BankCard(int n, string bank, Client* owner, int PIN) {
	this->number = n;
	this->bank = bank;
	this->owner = owner;
	this->PIN = PIN;

	this->isBlocked = false;
	this->money = 0;
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

bool BankCard::checkPIN(int enteredPIN) {
	if (this->isBlocked) return false;

	return (this->PIN == enteredPIN) ? true : false;
}

void BankCard::setBlocked() {
	this->isBlocked = true;
}