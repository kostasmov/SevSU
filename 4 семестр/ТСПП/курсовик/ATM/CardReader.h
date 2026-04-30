#pragma once
#include "BankCard.h"

class CardReader
{
public:
    BankCard* card;
    CardReader() { card = NULL; };

    bool setCard(BankCard* card);
    bool getbackCard();     // возврат карты

    bool isCardPresent();   // проверка наличия карты
    void getCardInfo();     // вывод информации о карте (надо бы перенести в ATM)

protected:
    //void sendAlert();
};

