#include "ATM.h"

// СЕССИЯ КЛИЕНТА (и студента(((
void ATM::startSession(Client* client) {
	cout << endl;
	cout << "--------------- " << this->bank << " ---------------";
	cout << endl << endl;

	BankCard* card = client->getCards()[0];	// НАДО НАПИСАТЬ ВЫБОР КАРТЫ?

	if (not this->setCardInReader(card)) {
		return;
	}

	this->getCardInfo();

	if (not this->validateCard()) {
		this->returnCardToUser();
		return;
	}

	this->getCardBalance();

	//this->deposit();

	this->returnCardToUser();
	cout << "BYE BUY !!!!!!!!!" << "\n\n";
}

// Установить карту в ридер
bool ATM::setCardInReader(BankCard* card) {
	cout << "Put your card in reader";
	cin.get();
	
	if (not this->cardReader.getCard(card)) {
		cout << "There's already card in reader!";
		cin.get();
		return 0;
	}
	
	cout << "Card is in reader" << "\n\n";
	return 1;
}

// Вернуть карту из ридера
void ATM::returnCardToUser() {
	if (this->cardReader.returnCard())
		cout << "Get your card back";
	else
		cout << "Can't return card - there's no card in reader";
	cin.get();
}


/*void ATM::tranferMoney() {

}*/


// Валидация (проверка) карты
bool ATM::validateCard() {
	if (this->cardReader.card->getBlockState()) {
		cout << "Sorry, card is blocked" << "\n\n";
		return 0;
	}

	for (int tries = 0; tries < 3; tries++) {
		int enteredPIN = this->keypad.enterPIN();

		if (this->cardReader.card->checkPIN(enteredPIN)) {
			cout << "Right! Cart validated" << "\n\n";
			return 1;
		}

		cout << "WRONG PIN" << endl;
	}

	cout << "Sorry, attempts ended. Card was blocked" << "\n\n";
	this->cardReader.card->setBlocked();

	return false;
}


// Вывод информации о карте
void ATM::getCardInfo() {
	// Идёт через прямое обращение к карте, ну и ладно
	cout << "Bank: " << this->cardReader.card->getBank() << endl;
	cout << "Number: " << this->cardReader.card->getNumber() << endl;
	cout << "Is card blocked: " << (this->cardReader.card->getBlockState() ? "YES" : "NO");
	cout << endl << endl;
}

// Вывод баланса на счёте клиента
void ATM::getCardBalance() {
	cout << "Balance: " << this->cardReader.card->getBalance();
	cin.get();
	cout << endl << endl;
}


/*void ATM::pickCommand(int code) {

}

void ATM::pickTransferOperation(int code) {

}*/


// внесение наличных
bool ATM::deposit() {
	return 0;
}

// снятие наличных
bool ATM::withdraw() {
	return 0;
}