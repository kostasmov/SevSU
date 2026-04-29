#pragma once

#include "Person.h"
#include <vector>
class BankCard;

class Client :
    public Person
{
public:
    Client(string name) : Person(name) {}

    void addCard(BankCard* card);
    vector<BankCard*> getCards();

protected:
    vector<BankCard*> cards;
};