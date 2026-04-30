#pragma once

#include <string>
using namespace std;

class Person
{
public:
    Person(string name) { this->name = name; };
    string getName() { return this->name; };

protected:
    string name;
};

