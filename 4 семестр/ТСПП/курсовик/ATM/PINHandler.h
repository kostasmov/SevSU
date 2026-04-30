#pragma once
#include "BankCard.h"

class PINHandler
{
public:
    PINHandler() {};
    void verifyPIN();

protected:
    //void enterPIN();
    void blockCard();
    void sendAlert();
};

