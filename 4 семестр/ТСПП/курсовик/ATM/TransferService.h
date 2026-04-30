#pragma once
#include "Recipient.h"
#include "BankCard.h"

class TransferService
{
public:
    TransferService() {};

    void rechargeCard(BankCard card, int sum);
    void chargeCard(BankCard card, int sum);
    void pickTransferOperation(int code);
    void transferToRecipient(Recipient* recipient);

protected:
    //Recipient* recipient;

    void setSum(int sum);
    void areBanksEqual();
    void setRecipient();
};

