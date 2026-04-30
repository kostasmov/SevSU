#pragma once

#include "Client.h"
#include <string>
using namespace std;

class BankCard
{
public:
    BankCard(int num, string bank, Client* owner, int PIN);

    // геттеры
    int getNumber() { return this->number; };
    string getBank() { return this->bank; };
    bool getBlockState() { return this->isBlocked; };
    double getBalance() { return this->money; };
    
    bool checkPIN(int enteredPIN);  // проверить PIN-код
    void setBlocked();              // заблокировать карту

    bool deposit(double amount);    // пополнение
    bool withdraw(double amount);   // снятие

protected:
    int number;     // номер карты
    string bank;    // банк
    Client* owner;  // клиент-владелец

    double money;   // деньги на счёте клиента

    int PIN;        // пин-код
    bool isBlocked; // заблокирована ли?
};
