#pragma once
#include "Person.h"

class Worker : public Person
{
public:
    int getID();
    //void getMessage(string text);

protected:
    int id;
};

