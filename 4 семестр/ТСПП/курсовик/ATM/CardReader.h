#pragma once
#include "BankCard.h"

class CardReader
{
public:
    void putCard(BankCard card);

    void getbackCard();

    //void isCardPresent();

    void getCardInfo();

protected:
    //bool isCardPresent = 0;
    BankCard card;

    void sendAlert();
};

