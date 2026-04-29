#pragma once

#include <string>
using namespace std;

class Person
{
public:
    Person(string name);
    //void startWorkWithATM(ATM atm);
    string getName();

protected:
    string name;
};

