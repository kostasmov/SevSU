#pragma once

#include <string>
#include "Client.h"
using namespace std;

class BankCard
{
public:
    void getBlockCheck();
    void getNumber();
    void checkPIN();
    //void setBlockState(void state);

protected:
    long int number;
    string validity;
    int PIN;
    string bank;
    Client owner;
    bool blockState = 1;
};
