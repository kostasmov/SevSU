#pragma once

#include "Person.h"
#include <vector>
#include <map>
class BankCard;

class Client :
    public Person
{
public:
    Client(string name) : Person(name) {}
    ~Client() {
        for (BankCard* card : cards) {
            delete card;
        }
    }

    void addCash(map<int, int> bills);  // добавить наличные
    map<int, int> getCash(int amount);  // взять часть наличных

    void addCard(BankCard* card) { this->cards.push_back(card); };  // добавить карту
    vector<BankCard*> getCards() { return this->cards; };           // доступ к картам
    
    string getRole() const override { return "client"; }



protected:
    vector<BankCard*> cards;
    map<int, int> cash = {};
};