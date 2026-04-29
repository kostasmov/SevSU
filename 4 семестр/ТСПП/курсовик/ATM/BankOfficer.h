#pragma once
#include "Worker.h"

class BankOfficer :
    public Worker
{
public:
    void sendMessage(Worker reciever);
};

