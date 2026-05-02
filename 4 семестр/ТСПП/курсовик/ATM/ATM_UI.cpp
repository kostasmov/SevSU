#include "ATM_UI.h"

void ATM_UI::showHello(const string& bank_name) {
	cout << endl;
	cout << "--------------- " << bank_name << " ---------------";
	cout << endl << endl;
}
void ATM_UI::showGoodbye() {
	cout << endl;
	cout << "--------------- " << "BYE-BYE!" << " ---------------";
	cout << endl << endl;
}

// Вывод сообщения
void ATM_UI::showMessage(const string& msg, bool waitInput) {
	cout << msg;
	if (waitInput) ATM_UI::waitForEnter();
	else cout << endl;
}

// Вывод инструкции (дополнительные ~~~)
void ATM_UI::showInstruction(const string& text) {
	cout << "~~~" << text << "~~~";
	ATM_UI::waitForEnter();
}


// Вывод информации о карте
void ATM_UI::showCardInfo(string bank, int num, bool blockState) {
	cout << endl;
	cout << "Bank: " << bank << endl;
	cout << "Number: " << num << endl;
	cout << "Is card blocked: " << (blockState ? "YES" : "NO");
	cout << endl << endl;
}

// Вывод баланса на карте (счёте)
void ATM_UI::showCardBalance(const double balance) {
	cout << endl;
	cout << "Balance: " << balance;
	ATM_UI::waitForEnter();
	cout << endl;
}


// Ввод PIN-кода
int ATM_UI::enterPIN() {
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


// Ожидание отклика пользователя (ENTER)
void ATM_UI::waitForEnter() {
	while (true) {
		int ch = _getch();

		if (ch == 13) {
			cout << endl;
			break;
		}
	}
}