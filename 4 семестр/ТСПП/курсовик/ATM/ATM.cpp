#include "ATM.h"
#include <iostream>
#include <conio.h>  // _getch()

ATM::ATM(string bank) {
	this->bank = bank;
}

string ATM::getBank() {
	return this->bank;
}

// СЕССИЯ КЛИЕНТА
void ATM::startSession(BankCard* card) {
	cout << endl;
	cout << "--------------- " << this->bank << " ---------------";
	cout << endl << endl;

	if (not this->putCard(card)) {
		cout << "There's already card in reader!";
		cin.get();
		return;
	}

	this->getCardInfo();

	if (not this->validateCard()) {
		this->getbackCard();
		return;
	}

}

// установить карту в ридер
bool ATM::putCard(BankCard* card) {
	if (this->cardReader.isCardPresent())
		return 0;
	
	cout << "Put your card in reader";
	cin.get();

	this->cardReader.setCard(card);
	cout << "Card is in reader" << "\n\n";
	return 1;
}

// возврат карты из ридера
void ATM::getbackCard() {
	if (not this->cardReader.getbackCard())
		cout << "Can't return card - there's no card in reader";
	else
		cout << "Get your card back";
	cin.get();
}

/*void ATM::tranferMoney() {

}*/

// проверка PIN-кода карты
bool ATM::validateCard() {
	if (this->cardReader.card->getBlockState()) return 0;

	for (int tries = 0; tries < 3; tries++) {
		
		int enteredPIN = this->enterPIN();

		if (this->cardReader.card->checkPIN(enteredPIN)) {
			cout << "Right! Cart validated" << "\n\n";
			return 1;
		}

		cout << "WRONG PIN" << endl;
	}

	cout << "Sorry, attempts ended. Card was blocked" << "\n\n";
	cardReader.card->setBlocked();

	return false;
}

// вывод информации о карте
int ATM::enterPIN() {
	string PIN;
	char ch;

	cout << "Enter PIN-code: ";

	// чтение посимвольно
	while (PIN.size() < 4) {
		ch = _getch();

		if (isdigit(ch)) {	// если цифра - считаем как часть PIN
			cout << '*';
			PIN += ch;   
		}

		// разрешить Backspace (код 8)
		else if (ch == 8 && PIN.length() > 0) {
			cout << "\b \b";	// стирание символа из консоли
			PIN.pop_back();	
		}
	}

	cout << endl;
	return stoi(PIN);
}

// вывод информации о карте
void ATM::getCardInfo() {
	cout << "Bank: " << this->cardReader.card->getBank() << endl;
	cout << "Number: " << this->cardReader.card->getNumber() << endl;
	cout << "Is card blocked: " << (this->cardReader.card->getBlockState() ? "YES" : "NO");
	cout << endl << endl;
}

// вывод баланса на счёте клиента
/*void ATM::getCardInfo() {
	cout << "Bank: " << this->cardReader.card->getBank() << endl;
	cout << "Number: " << this->cardReader.card->getNumber() << endl;
	cout << "Is card blocked: " << (this->cardReader.card->getBlockState() ? "YES" : "NO");
	cout << endl << endl;
}*/

/*void ATM::pickCommand(int code) {

}

void ATM::pickTransferOperation(int code) {

}*/