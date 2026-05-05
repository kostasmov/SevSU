#include "ATM.h"

// ================== ИНТЕРФЕЙС / СИСТЕМА ==================
void ATM::startSession(Client* client) {
	this->ui.showHello(this->bank);

	// -----------------
	BankCard* card = client->getCards()[0];
	// -----------------

	// проверить вставляется ли карта в ридер
	if (!this->setCardInReader(card)) {
		return;
	}

	// вывести информацию о карте
	this->getCardInfo();	

	// валидация карты (ввод PIN-кода)
	if (!this->validateCard()) {
		this->returnCardToUser();
		return;
	}

	// -----------------
	// КЛИЕНТ ДОЛЖЕН ВЫБИРАТЬ ОПЕРАЦИЮ
	while (this->pickCommand()) {};
	// -----------------

	//// вывод баланса на счёте клиента
	//this->getCardBalance();

	//// пополнение счёта (внесение наличных)
	//this->makeDeposit();

	//// пополнение счёта (внесение наличных)
	//this->makeWithdraw();

	// вернуть карту
	this->returnCardToUser();

	this->ui.showGoodbye();
}

int ATM::pickCommand() {

	this->ui.nextBlock();

	this->ui.showLine();
	this->ui.showMessage("Show card balance - 1", 0);
	this->ui.showMessage("Make dispence - 2", 0);
	this->ui.showMessage("Make withdraw - 3", 0);
	this->ui.showMessage("Exit the system - 0", 0);
	this->ui.showLine();

	int operCode = this->ui.enterNumber(2, "Enter operation code");

	switch (operCode) {
	case (0):
		cout << "0000000000000000000\n";
		return 0;
	case (1):
		cout << "1111111111111111\n";
		break;
	case (2):
		cout << "2222222222222222\n";
		break;
	default:
		cout << "YOU ARE FUCKING MORON\n";
	}

	return 1;
}


// ================== ДЕЙСТВИЯ С КАРТОЙ ==================

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


// ================== ОПЕРАЦИИ С ДЕНЬГАМИ И СЧЁТОМ ==================

// Вывод информации о карте
void ATM::getCardInfo() {
	// ...идёт через прямое обращение к карте, ну и ладно
	this->ui.showCardInfo(this->cardReader.card->getBank(),
		this->cardReader.card->getNumber(),
		this->cardReader.card->getBlockState());

	ATM_UI::showInstruction("Continue");
}

// Вывод баланса на счёте клиента
void ATM::getCardBalance() {
	this->ui.showCardBalance(this->cardReader.card->getBalance());
}

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

	while (true) {
		int amount = this->ui.enterNumber(6, "Enter money amount");

		// проверить есть ли в кассе достаточно нала
		if (!this->cashHandler.canDispenseAmount(amount)) {
			this->ui.showMessage("Sorry, can't dispense this money amount!");
			if (!this->ui.enterTrueFalse("Try another number?"))
				return 0;
			continue;
		}

		this->ui.showMessage("Correct amount", false);
		if (!this->ui.enterTrueFalse("Continue operation?"))
			return 0;

		// -------- СНЯТИЕ НАЛИЧНЫХ --------
		if (!this->cardReader.card->withdraw(amount)) {	// проверка баланса
			this->ui.showMessage("Sorry, you have no money");
			return 0;
		}

		auto cash = this->cashHandler.cashOut(amount);
		this->billAcceptor.returnCash();

		this->ui.showMessage("Operation done!");
		// ---------------------------------

		this->ui.showInstruction("Take your money away NOW");
		return 1;
	}
}