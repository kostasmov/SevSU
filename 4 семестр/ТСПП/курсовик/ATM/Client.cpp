#include "Client.h"

void Client::addCash(map<int, int> bills) {
	for (const auto [key, value] : bills) {
		this->cash[key] += value;
	}
}

map<int, int> Client::getCash(int amount) {
	// АБСОЛЮТНАЯ ЗАГЛУШКА - у клиента БЕСКОНЕЧНЫЕ ДЕНЬГИ
    map<int, int> cash;
    
    vector<int> denominations = { 5000, 2000, 1000, 500, 200, 100, 50 };
    
    int remaining = amount;

    for (int d : denominations) {
        int need = remaining / d;

        remaining -= need * d;
        cash[d] = need;
    }

    return cash;
}