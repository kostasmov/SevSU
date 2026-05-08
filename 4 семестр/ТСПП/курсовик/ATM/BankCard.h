#pragma once

#include "Client.h"
#include <string>
using namespace std;

class BankCard
{
public:
    BankCard(string num, string bank, Client* owner, int PIN);
    ~BankCard() {};

    string getNumber();     // геттеры
    string getBank();
    string getOwner();

    bool getBlockState();
    double getBalance();
    
    bool checkPIN(int enteredPIN);  // проверить PIN-код
    void setBlocked();              // заблокировать карту

    bool deposit(double amount);    // пополнение
    bool withdraw(double amount);   // снятие

protected:
    string number;  // номер карты
    string bank;    // банк
    Client* owner;  // клиент-владелец

    double money;   // деньги на счёте клиента

    int PIN;        // пин-код
    bool isBlocked; // заблокирована ли?
};
