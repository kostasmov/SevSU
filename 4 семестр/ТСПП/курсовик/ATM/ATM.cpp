#include "ATM.h"

// СЕССИЯ КЛИЕНТА (и студента(((
void ATM::startSession(Client* client) {
	this->ui.showHello(this->bank);

	// -----------------
	BankCard* card = client->getCards()[0];
	// -----------------

	// проверить вставляется ли карта в ридер
	if (not this->setCardInReader(card)) {
		return;
	}

	// вывести информацию о карте
	this->getCardInfo();	

	// валидация карты (ввод PIN-кода)
	if (not this->validateCard()) {
		this->returnCardToUser();
		return;
	}

	// -----------------
	// КЛИЕНТ ДОЛЖЕН ВЫБИРАТЬ ОПЕРАЦИЮ
	// -----------------

	// вывод баланса на счёте клиента
	this->getCardBalance();

	// пополнение счёта (внесение наличных)
	this->makeDeposit();

	// пополнение счёта (внесение наличных)
	this->makeWithdraw();

	// вернуть карту
	this->returnCardToUser();

	this->ui.showGoodbye();
}

// Установить карту в ридер
bool ATM::setCardInReader(BankCard* card) {
	this->ui.showInstruction("Put your card in reader");
	
	// проверить не занят ли ридер
	if (!this->cardReader.getCard(card)) {
		this->ui.showMessage("There's already card in reader!");
		return 0;
	}
	
	this->ui.showMessage("Card read successfully!");
	return 1;
}

// Вернуть карту из ридера
void ATM::returnCardToUser() {
	if (this->cardReader.returnCard())
		this->ui.showInstruction("Get your card back!");
	else
		this->ui.showMessage("Can't return card - there's no card in reader!");
}


/*void ATM::tranferMoney() {

}*/


// Валидация (проверка) карты
bool ATM::validateCard() {
	// проверить не заблокирована ли карта
	if (this->cardReader.card->getBlockState()) {
		this->ui.showMessage("Sorry, card is blocked");
		return 0;
	}

	// три попытки на ввод
	for (int tries = 0; tries < 3; tries++) {
		int enteredPIN = this->ui.enterPIN();

		if (this->cardReader.card->checkPIN(enteredPIN)) {
			this->ui.showMessage("Right! Cart validated");
			return 1;
		}

		this->ui.showMessage("WRONG PIN", false);
	}

	this->ui.showMessage("Sorry, attempts ended. Card was blocked");
	this->cardReader.card->setBlocked();

	return false;
}


// Вывод информации о карте
void ATM::getCardInfo() {
	// ...идёт через прямое обращение к карте, ну и ладно
	this->ui.showCardInfo(this->cardReader.card->getBank(),
		this->cardReader.card->getNumber(),
		this->cardReader.card->getBlockState());
}


// Вывод баланса на счёте клиента
void ATM::getCardBalance() {
	this->ui.showCardBalance(this->cardReader.card->getBalance());
}


/*void ATM::pickCommand(int code) {

}

void ATM::pickTransferOperation(int code) {

}*/


// Внесение наличных
bool ATM::makeDeposit() {
	// проверить помещается ли в банкомат хоть что-то
	if (!this->cashHandler.canAcceptBanknotes(5)) {
		this->ui.showMessage("Sorry, cashbox is FULL of money");
		return 0;
	}

	this->ui.showInstruction("Put money in bill acceptor");

	// -----------------
	map<int, int> cash;
	cash[100] = 5;
	cash[500] = 3;
	cash[1000] = 1;
	// -----------------

	// попытка передать нал и обработка результата
	switch (this->billAcceptor.getCash(&cash)) {
	case 404:
		this->ui.showMessage("Error: Too many banknotes inserted (404)", false);
		break;

	case 405:
		this->ui.showMessage("Error: Validation failed (405)", false);
		break;

	case 1:	// транзакцию можно провести
		this->ui.showMessage("Cash accepted successfully", false);
		if (this->depositTransaction()) return 1;
		break;

	default:
		this->ui.showMessage("Unknown error while accepting cash", false);
		break;
	}

	this->ui.showInstruction("Get your cash back!");
	return 0;
}
bool ATM::depositTransaction() {
	int cashSum = this->billAcceptor.calculateCash();
	int banknotesAmount = this->billAcceptor.countBanknotes();

	this->ui.showMessage("Money put into - " + to_string(cashSum), false);
	if (!this->ui.enterTrueFalse("Continue operation?")) return 0;

	// --------- ТРАНЗАКЦИЯ ---------
	bool done = this->cashHandler.cashIn(this->billAcceptor.cash, banknotesAmount);
	if (!done) {
		this->ui.showMessage("Sorry, there's no place in cashbox");
		return 0;
	}

	this->cardReader.card->deposit(cashSum);
	this->billAcceptor.takeCashInHandler();

	this->ui.showMessage("Operation completed!", false);
	this->ui.showInstruction("Take your CHECK paper");

	return 1;
}


// Снятие наличных
bool ATM::makeWithdraw() {
	// проверить не пустая ли касса
	if (!this->cashHandler.canDispenseAmount(100)) {
		this->ui.showMessage("Sorry, no money((");
		return 0;
	}

	int amount;

	while (true) {
		amount = this->ui.enterAmount();

		if (this->cashHandler.canDispenseAmount(amount)) {
			this->ui.showMessage("Correct amount", false);
			
			if (this->ui.enterTrueFalse("Contrinue operation?")) {
				// ТРАНЗАКЦИЯ

				this->ui.showMessage("Transaction done!");
				return 1;
			}
			
			return 0;
		}

		this->ui.showMessage("Sorry, can't dispense this money amount!");
		if (!this->ui.enterTrueFalse("Try another number?")) break;
	}
	
	return 0;
}