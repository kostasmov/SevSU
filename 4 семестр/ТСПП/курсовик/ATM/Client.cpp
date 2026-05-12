#include "Client.h"

// Добавление клиенту наличных
int Client::depositCash(map<int, int> banknotes) {
	return this->recordDeposit(banknotes);
}

// Клиент отдаёт наличные
map<int, int> Client::withdrawCash(int moneyAmount) {
    // ЗАГЛУШКА - у клиента БЕСКОНЕЧНЫЕ ДЕНЬГИ
    map<int, int> cash;

    int remaining = moneyAmount;

    for (int d : this->denominations) {
        int need = remaining / d;
        remaining -= need * d;
        cash[d] = need;
    }

    return cash;
}

