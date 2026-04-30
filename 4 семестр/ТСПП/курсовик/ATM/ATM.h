#pragma once

#include "CardReader.h"
#include "CashHandler.h"
#include "BillAcceptor.h"
#include "TransferService.h"
#include "InputModule.h"

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
    //TransferService transfer;   // 
    const InputModule keypad;   // Блок ввода (кнопки)

    bool setCardInReader(BankCard* card); 
    void returnCardToUser();

    bool validateCard();    // проверка безопасности

    void getCardInfo();     // вывод информации о карте
    void getCardBalance();  // вывод баланса на карте

    bool deposit();     // пополнить карту
    bool withdraw();    // снять кэш

    //void pickCommand(int code);
    //void pickTransferOperation(int code);
};

