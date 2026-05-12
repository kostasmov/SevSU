#include "ATM.h"

// ================== ИНТЕРФЕЙС / СИСТЕМА ==================
void ATM::startSession(Client* client, BankCard* card) {
	this->ui.showHello(this->bank);

	// проверить вставляется ли карта в ридер
	if (!this->setCardInReader(card)) return;

	// вывести информацию о карте
	this->showCardInfo();	

	// валидация карты (ввод PIN-кода)
	/*bool validated = this->validateCard();

	if (!validated) {
		this->returnCardToUser();
		this->ui.showGoodbye();
		return;
	}*/

	// ---------------------------------
	while (true) {
		switch (this->pickUserCommand()) {
		case(0):
			// завершение работы
			this->returnCardToUser();
			this->ui.showGoodbye();
			return;

		case (1):
			// вывод баланса на счёте клиента
			this->getCardBalance();
			break;

		case (2):
			// пополнение счёта (внесение наличных)
			this->makeDeposit(client->withdrawCash(
				this->ui.enterNumber(6, "How much money you want to put into")
			));
			break;

		case (3):
			// снятие со счёта (выдача наличных)
			this->makeWithdraw();
			break;

		default:
			this->ui.showMessage("Wrong operation code, try again");
		};
	}
	// ---------------------------------
}
void ATM::startSession(Collector* client) {
	this->ui.showHello(this->bank);

	while (true) {
		switch (this->pickCollectorCommand()) {
		case(0):
			// завершение работы
			this->ui.showGoodbye();
			return;

		case (1):
			// проверка содержимого кассы
			this->ui.showCashboxInfo(
				this->cashHandler.countBanknotes(), 
				this->cashHandler.getCashInfo()
			);
			break;

		case (2):
			// проверка картоприёмника
			if (this->cardReader.card) {
				this->ui.showMessage("There's a forbidden card in Reader");
				this->returnCardToUser();
			}
			else this->ui.showMessage("---- Reader is empty ----");
			break;

		case (3):
			if (this->billAcceptor.calculateCash() > 0) {
				this->ui.showMessage("There's a forbidden cash in acceptor");
				this->billAcceptor.withdrawCash();
				this->ui.showInstruction("Take these money away");
			}
			else this->ui.showMessage("---- Bill acceptor is empty ----");
			break;

		case (4):
			break;

		case (5):
			break;

		default:
			this->ui.showMessage("Wrong operation code, try again");
		};
	}
}

int ATM::pickUserCommand() {
	vector<string> options = {
		"Show card balance",
		"Make deposit",
		"Make withdraw",
	};

	return ATM_UI::showChoiseMenu(
		options,
		"",
		"Enter operation code"
	);
}
int ATM::pickCollectorCommand() {
	vector<string> options = {
		"Check banknotes",
		"Check card reader",
		"Check bill acceptor",
		"Deposit money in cashbox",
		"Take money out of cashbox"
	};

	return ATM_UI::showChoiseMenu(
		options,
		"Choose operation",
		"Enter operation code",
		false
	);
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
		return false;
	}

	// три попытки на ввод
	for (int tries = 0; tries < 3; tries++) {
		int enteredPIN = this->ui.enterPIN();

		if (this->cardReader.card->checkPIN(enteredPIN)) {
			this->ui.showMessage("Right! Cart validated");
			return true;
		}

		this->ui.showMessage("WRONG PIN", false);
	}

	this->ui.showMessage("Sorry, attempts ended. Card was blocked");
	this->cardReader.card->setBlocked();

	return false;
}


// ================== ОПЕРАЦИИ С ДЕНЬГАМИ И СЧЁТОМ ==================

// Вывод информации о карте
void ATM::showCardInfo() {
	// ...идёт через прямое обращение к карте, ну и ладно
	this->ui.showCardInfo(
		this->cardReader.card->getBank(),
		this->cardReader.card->getNumber(),
		this->cardReader.card->getBlockState()
	);

	ATM_UI::showInstruction("Continue");
}


// Вывод баланса на счёте клиента
void ATM::getCardBalance() {
	this->ui.showCardBalance(this->cardReader.card->getBalance());
}


// Внесение наличных
bool ATM::makeDeposit(map<int, int> cash) {
	// проверить помещается ли в банкомат хоть что-то
	//if (!this->cashHandler.canAccept(3)) {
	//	this->ui.showMessage("Sorry, cashbox is FULL of money");
	//	return 0;
	//}

	this->ui.showInstruction("Put money in bill acceptor");

	// попытка передать нал и обработка результата
	switch (this->billAcceptor.depositCash(cash)) {
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
	}

	this->billAcceptor.withdrawCash();
	this->ui.showInstruction("Get your cash back!");

	return 0;
}
bool ATM::depositTransaction() {
	int cashSum = this->billAcceptor.calculateCash();
	this->ui.showMessage("Money put into - " + to_string(cashSum), false);

	if (!this->ui.enterTrueFalse("Continue operation?")) return 0;

	// --------- ПЕРЕВОД (ПОПОЛНЕНИЕ) ---------
	bool done = this->billAcceptor.takeCashInHandler(this->cashHandler);

	if (!done) {
		this->ui.showMessage("Sorry, there's no place in cashbox");
		return false;
	}

	this->cardReader.card->deposit(cashSum);

	this->ui.showMessage("Operation completed!", false);
	this->ui.showInstruction("Take your CHECK paper");

	return true;
}


// Снятие наличных
bool ATM::makeWithdraw() {
	// проверить не пустая ли касса
	if (this->cashHandler.countBanknotes() <= 0) {
		this->ui.showMessage("Sorry, ATM has no money((");
		return false;
	}

	while (true) {
		int amount = this->ui.enterNumber(6, "Enter money amount");

		// проверить есть ли в кассе достаточно наличных
		if (!this->cashHandler.canDispense(amount)) {
			this->ui.showMessage("Sorry, can't dispense this money amount!");
			if (!this->ui.enterTrueFalse("Try another number?"))
				return 0;
			continue;
		}

		this->ui.showMessage("Correct amount", false);
		if (!this->ui.enterTrueFalse("Continue operation?"))
			return 0;

		// -------- СНЯТИЕ НАЛИЧНЫХ --------
		bool done = this->cardReader.card->withdraw(amount);

		if (!done) {	// проверка что операция прошла (баланса хватило)
			this->ui.showMessage("Sorry, you have no money");
			return false;
		}

		this->cashHandler.withdrawCash(amount);
		// здесь мог быть программный код
		this->billAcceptor.withdrawCash();

		this->ui.showMessage("Operation done!");
		// ---------------------------------

		this->ui.showInstruction("Take your money away NOW");
		return true;
	}
}