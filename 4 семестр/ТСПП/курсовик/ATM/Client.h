#pragma once
#include "Person.h"

class BankCard;

class Client : 
    public Person
{
public:
    void addCard(BankCard card);

protected:
    //BankCard cards;
};

