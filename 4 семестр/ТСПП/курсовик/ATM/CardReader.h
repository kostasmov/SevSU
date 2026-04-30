#pragma once
#include "BankCard.h"

class CardReader
{
public:
    BankCard* card;

    CardReader() { card = NULL; };

    bool getCard(BankCard* card);   // ридер принимает карту
    bool returnCard();              // ридер отдаёт карту

    bool isCardPresent() const; // проверка наличия карты
    void getCardInfo();         // возрат информации о карте (НЕ РАБОТАЕТ)

protected:
    //void sendAlert();
};

