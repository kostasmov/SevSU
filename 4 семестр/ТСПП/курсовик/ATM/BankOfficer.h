#pragma once
#include "Worker.h"

class BankOfficer :
    public Worker
{
public:
    BankOfficer(string name, int id) : Worker(name, id) {}
    ~BankOfficer() {}

    string getRole() const override { return "officer"; }
};
