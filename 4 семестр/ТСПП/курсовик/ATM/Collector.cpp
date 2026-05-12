#include "Collector.h"

// Добавление наличных
int Collector::depositCash(map<int, int> banknotes) {
    return this->recordDeposit(banknotes);
}

// Инкассатор может БЕСКОНЕЧНО МНОГО выдавать наличные
map<int, int> Collector::withdrawCash(int moneyAmount) {
    map<int, int> cash;

    int remaining = moneyAmount;

    for (int d : this->denominations) {
        int need = remaining / d;
        remaining -= need * d;
        cash[d] = need;
    }

    return cash;
}