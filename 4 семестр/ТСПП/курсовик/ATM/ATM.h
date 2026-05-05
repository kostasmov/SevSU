#pragma once

#include "CardReader.h"
#include "CashHandler.h"
#include "BillAcceptor.h"
#include "TransferService.h"
#include "ATM_UI.h"

#include <string>
#include <iostream>

using namespace std;

// МОДЕЛИРОВАНИЕ БАНКОМАТА

class ATM
{
public:
    ATM(string bank) { this->bank = bank; };
    string getBank() { return this->bank; };

    void startSession(Client* client);  // Начать сеанс обслуживания клиента

    //void tranferMoney();

protected:
    string bank;

    CardReader cardReader;      // Картоприёмник
    CashHandler cashHandler;    // Касса
    BillAcceptor billAcceptor;  // Деньгоприёмник
    const ATM_UI ui;            // Блок ввода/вывода

    bool setCardInReader(BankCard* card); 
    void returnCardToUser();

    bool validateCard();    // проверка безопасности

    void getCardInfo();     // вывод информации о карте
    void getCardBalance();  // вывод баланса на карте

    bool makeDeposit();         // пополнить карту
    bool depositTransaction();  // перевод средств + пополнение кассы

    bool makeWithdraw();    // снять кэш

    int pickCommand();
    //void pickTransferOperation(int code);
};

