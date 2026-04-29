#pragma once
#include "BankCard.h"

class PINHandler
{
public:
    void verifyPIN(BankCard card);

protected:
    void enterPIN();
    void blockCard();
    void sendAlert();
};

