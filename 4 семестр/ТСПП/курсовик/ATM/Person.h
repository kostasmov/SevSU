#pragma once

#include <string>
using namespace std;

class Person
{
public:
    Person(string name) { this->name = name; };
    virtual ~Person() {};

    virtual string getRole() const = 0;

    string getName() { return this->name; };

protected:
    string name;
};

