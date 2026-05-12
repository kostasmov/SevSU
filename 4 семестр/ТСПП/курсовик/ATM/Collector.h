#pragma once

#include "Worker.h"
#include "CashHolder.h"

class Collector :
    public Worker, public CashHolder
{
public:
    Collector(string name, int id) : Worker(name, id) {}
    ~Collector() {}

    string getRole() const override { return "collector"; }

    int depositCash(map<int, int> banknotes) override;     // добавить наличные
    map<int, int> withdrawCash(int moneyAmount) override;   // отдать наличные
};

