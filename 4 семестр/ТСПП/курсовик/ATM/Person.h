#pragma once

#include <string>
using namespace std;

// ЧЕЛОВЕК - ПОЛЬЗОВАТЕЛЬ СИСТЕМЫ

class Person
{
public:
    Person(string name) { this->name = name; };
    virtual ~Person() {};

    // роль пользователя определяется классами-наследниками
    virtual string getRole() const = 0;

    string getName() { return this->name; };

protected:
    string name;
};

