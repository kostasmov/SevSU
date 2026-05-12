#include "ATM_UI.h"

void ATM_UI::showHello(const string& bank_name) {
	cout << endl;
	cout << "--------------- " << bank_name << " ---------------";
	cout << endl;
}
void ATM_UI::showGoodbye() {
	cout << endl;
	cout << "--------------- " << "BYE-BYE!" << " ---------------";
	cout << endl;
}
void ATM_UI::showLine() {
	cout << "----------------------------------------" << endl;
}

// Вывод сообщения
void ATM_UI::showMessage(const string& msg, bool waitInput) {
	cout << msg;
	if (waitInput) ATM_UI::waitForEnter();
	else cout << endl;
}

// Вывод инструкции (дополнительные ~~~)
void ATM_UI::showInstruction(const string& text) {
	cout << endl;
	cout << "~~~" << text << "~~~";
	ATM_UI::waitForEnter();
}

// Вывод меню с выбором операций
int ATM_UI::showChoiseMenu(const vector<string>&options,
	const string& title, const string& msg,
	const bool showLines)
{
	if (showLines) {
		cout << endl; 
		ATM_UI::showLine();
	}
	else cout << endl;

	if (!title.empty()) cout << title << ": " << endl;

	for (int i = 0; i < options.size(); i++) {
		cout << "   " << i + 1 << " - " << options[i] << endl;
	}
	
	if (!showLines) cout << "   ----------------------------------" << endl;
	cout << "   0 - Exit" << endl;

	if (showLines) ATM_UI::showLine(); 
	else cout << endl;

	while (true) {
		int choice = ATM_UI::enterNumber(2, msg);

		if (choice >= 0 && choice <= options.size()) {
			return choice;
		}
	}
}


// ======================= ОПЕРАЦИИ ВЫВОДА =======================

// Преобразование номера карты (ДЛЯ ВЫВОДА)
string ATM_UI::formatCardNumber(const string& num) {
	string result;
	for (int i = 0; i < num.size(); i++) {
		result += num[i];
		if ((i + 1) % 4 == 0 && i + 1 != num.size()) {
			result += ' ';
		}
	}
	return result;
}

// Вывод информации о карте
void ATM_UI::showCardInfo(string bank, string num, bool blockState) {
	cout << endl;
	cout << "Bank: " << bank << endl;
	cout << "Number: " << formatCardNumber(num) << endl;
	cout << "Is card blocked: " << (blockState ? "YES" : "NO");
	cout << endl;
}

// Вывод баланса на карте (счёте)
void ATM_UI::showCardBalance(const double balance) {
	cout << endl;
	cout << "Balance: " << balance;
	ATM_UI::waitForEnter();
	//cout << endl;
}

// Вывод информации о содержимом кассы
void ATM_UI::showCashboxInfo(int billsCount, map<int, int> bills) {
	cout << endl;
	cout << "Cashbox keeps " + to_string(billsCount) + " banknotes:" << endl;

	for (const auto& [denomination, count] : bills) {
		cout << setw(3) << "" <<
			left << setw(4) << denomination 
			<< " : " << count << endl;
	}
}

// ======================= ОПЕРАЦИИ ВВОДА =======================

// Ввод PIN-кода
int ATM_UI::enterPIN() {
	string PIN;
	char ch;

	cout << endl << "Enter PIN-code: ";

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

// Ввод числа (деньги или код операции)
int ATM_UI::enterNumber(int max, string msg) {
	string input;
	char ch;

	if (!msg.empty()) cout << msg << " - ";

	while (true) {
		ch = _getch();

		if (ch == '\r' && input.size() > 0) {	// Enter - конец ввода
			cout << endl;
			break;
		}
		else if (ch == '\b') {	// Backspace
			if (!input.empty()) {
				input.pop_back();
				cout << "\b \b";	// удаляем символ с экрана
			}
		}
		else if (isdigit(ch) && input.size() < max) {
			input.push_back(ch);
			cout << ch;
		}
	}

	return stoi(input);
}

// Ввод true/false (подтверждение операции)
bool ATM_UI::enterTrueFalse(string msg) {
	cout << endl;
	if (!msg.empty()) cout << msg << endl;
	cout << "Enter t/f: ";

	char ch;
;
	while (true) {
		ch = _getch();

		/*if (ch == '\r') {
			continue;
		}
		else if (ch == '\b') {
			continue;
		}
		else {*/
		ch = tolower(ch);	// приводим к нижнему регистру
		if (ch == 't' || ch == 'f') {
			cout << ch << endl;
			return ch == 't';
		}
		//}
	}
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