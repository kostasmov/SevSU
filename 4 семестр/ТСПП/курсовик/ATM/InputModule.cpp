#include "InputModule.h"

int InputModule::enterPIN() {
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
