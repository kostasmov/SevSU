#pragma once

#include <vector>
#include <map>

#include "Person.h"
#include "CashHolder.h"

class BankCard;

class Client :
    public Person, public CashHolder
{
public:
    Client(string name) : Person(name) {}
    ~Client() {
        for (BankCard* card : cards) { 
            delete card;
        }
    }

    void addCard(BankCard* card) { this->cards.push_back(card); };  // добавить карту
    vector<BankCard*> getCards() { return this->cards; };           // доступ к картам
    
    string getRole() const override { return "client"; }

    int depositCash(map<int, int> banknotes) override;      // добавить наличные
    map<int, int> withdrawCash(int moneyAmount) override;   // отдать наличные

protected:
    vector<BankCard*> cards;    // банковские карты
};