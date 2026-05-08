#pragma once

#include "CardReader.h"
#include "CashHandler.h"
#include "BillAcceptor.h"
#include "Collector.h"
#include "ATM_UI.h"

#include <string>
using namespace std;

// МОДЕЛИРОВАНИЕ БАНКОМАТА

class ATM
{
public:
    ATM(string bank) { this->bank = bank; };
    string getBank() { return this->bank; };

    void startSession(Client* user, BankCard* card);  // Начать сеанс обслуживания
    void startSession(Collector* user);

protected:
    string bank;

    CardReader cardReader;      // Картоприёмник
    CashHandler cashHandler;    // Касса
    BillAcceptor billAcceptor;  // Деньгоприёмник
    const ATM_UI ui;            // Блок ввода/вывода

    int pickUserCommand();      // Выбор команды (зависит от роли)
    int pickCollectorCommand();

    bool setCardInReader(BankCard* card); 
    void returnCardToUser();

    bool validateCard();        // проверка безопасности

    void showCardInfo();        // вывод информации о карте
    void getCardBalance();      // вывод баланса на карте

    bool makeDeposit(map<int, int> cash);   // пополнить карту
    bool depositTransaction();              // перевод средств + пополнение кассы

    bool makeWithdraw();        // снять наличные
};

