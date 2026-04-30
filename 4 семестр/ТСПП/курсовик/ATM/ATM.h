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
    string getBank();   // узнать банк

    void startSession(BankCard* card);

    bool putCard(BankCard* card);
    void getbackCard();

    void getCardInfo(); // вывод информации о карте 

    int enterPIN();     // ввод PIN-кода

    void tranferMoney();

protected:
    string bank;

    CardReader cardReader;
    CashHandler cashHandler;
    BillAcceptor billAcceptor;
    TransferService transfer;
    //PINHandler PINhandler;

    bool validateCard();

    //void pickCommand(int code);
    //void pickTransferOperation(int code);
};

