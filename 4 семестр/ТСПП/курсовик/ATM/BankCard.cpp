#include "BankCard.h"

BankCard::BankCard(int n, string bank, Client* owner, int PIN) {
	this->number = n;
	this->bank = bank;
	this->owner = owner;
	this->PIN = PIN;

	this->isBlocked = false;
	this->money = 0;
}

// доступ к параметрам (гетры)
int BankCard::getNumber() { return this->number; }				// номер карты
string BankCard::getBank() { return this->bank; }				// банк
string BankCard::getOwner() { return this->owner->getName(); }	// имя владельца

bool BankCard::getBlockState() { return this->isBlocked; }		// заблокирована ли?
double BankCard::getBalance() { return this->money; }			// баланс


// пополнение баланса
bool BankCard::deposit(double amount) {
	this->money += amount;
	return 1;
}

// снятие денег со счёта
bool BankCard::withdraw(double amount) {
	if (this->money >= amount) {
		this->money -= amount;
		return 1;
	}

	return 0;
}

// сверить введённый PIN с реальным
bool BankCard::checkPIN(int enteredPIN) {
	if (this->isBlocked) return false;

	return (this->PIN == enteredPIN) ? true : false;
}

// заблокировать карту
void BankCard::setBlocked() {
	this->isBlocked = true;
}