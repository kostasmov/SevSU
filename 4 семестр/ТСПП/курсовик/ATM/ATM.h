#pragma once

#include "CardReader.h"
#include "CashHandler.h"
#include "BillAcceptor.h"
#include "TransferService.h"
#include "PINHandler.h"

#include <string>
using namespace std;

class ATM
{
public:
    ATM(string bank);

    void getBank();
    void startSession();
    void putCard();
    void getbackCard();
    void tranferMoney();

protected:
    string bank;

    CardReader cardReader;
    CashHandler cashRegister;
    BillAcceptor billAcceptor;
    TransferService transfer;
    PINHandler PINhandler;

    void pickCommand(int code);
    void pickTransferOperation(int code);
};

