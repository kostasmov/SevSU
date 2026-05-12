#pragma once

#include "Person.h"

class Worker : public Person
{
public:
    Worker(string name, int id) : Person(name) { this->id = id; }
    virtual ~Worker() {};

    int getID() const { return this->id; };

protected:
    int id; // идентификатор
};

