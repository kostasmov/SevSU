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
    
    //void checkPIN();
    //void setBlockState(void state);

protected:
    int number;
    string bank;
    Client* owner;

    int PIN;
    bool isBlocked;
    //string validity;
};
