#pragma once

#include <iostream>
#include <string>
#include <conio.h>  // _getch()

using namespace std;

class ATM_UI
{
public:
    ATM_UI() {};

    static void showHello(const string& bank_name);
    static void showGoodbye();

    static void showMessage(const string& msg, bool wait=true);
    static void showInstruction(const string& msg);

    static void showCardInfo(string bank, int num, bool blockState);
    static void showCardBalance(const double balance);

    static int enterPIN();

protected:
    static void waitForEnter();
};
