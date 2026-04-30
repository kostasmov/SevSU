#include "BankCard.h"

BankCard::BankCard(int n, string bank, Client* owner, int PIN) {
	this->number = n;
	this->bank = bank;
	this->owner = owner;
	this->PIN = PIN;

	this->isBlocked = false;
	this->money = 0;
}

// пополнение баланса
bool BankCard::deposit(double amount) {
	this->money += amount;
	return 1;
}

// транжирим денюшшки(((
bool BankCard::withdraw(double amount) {
	if (this->money >= amount) {
		this->money -= amount;
		return 1;
	}

	return 0;
}

/*bool BankCard::getBlockState() {
	return this->isBlocked;
}

int BankCard::getNumber() {
	return this->number;
}

string BankCard::getBank() {
	return this->bank;
}

double BankCard::getBalance() {
	return this->money;
}*/

bool BankCard::checkPIN(int enteredPIN) {
	if (this->isBlocked) return false;

	return (this->PIN == enteredPIN) ? true : false;
}

void BankCard::setBlocked() {
	this->isBlocked = true;
}