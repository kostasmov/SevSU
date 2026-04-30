#pragma once

#include "CardReader.h"
#include "CashHandler.h"
#include "BillAcceptor.h"
#include "TransferService.h"

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

    void tranferMoney();

protected:
    string bank;

    CardReader cardReader;
    CashHandler cashHandler;
    BillAcceptor billAcceptor;
    TransferService transfer;

    bool validateCard();    // проверка безопасности
    int enterPIN();         // ввод PIN-кода

    void getCardInfo();     // вывод информации о карте
    void getCardBalance();  // вывод баланса на карте

    bool deposit();     // пополнить карту
    bool withdraw();    // снять кэш

    //void pickCommand(int code);
    //void pickTransferOperation(int code);
};

