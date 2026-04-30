#pragma once

#include "Client.h"
#include <string>
using namespace std;

class BankCard
{
public:
    BankCard(int num, string bank, Client* owner, int PIN);

    int getNumber();
    string getBank();
    bool getBlockState();
    
    bool checkPIN(int enteredPIN);
    void setBlocked();

protected:
    int number;
    string bank;
    Client* owner;

    double money;  // деньги на счёте клиента

    int PIN;
    bool isBlocked;
};
