#pragma once

#include <iostream>
#include <string>
#include <cctype>
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
    static int enterAmount();
    static bool enterTrueFalse(string msg="");

protected:
    static void waitForEnter();
};
