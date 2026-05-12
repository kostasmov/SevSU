#pragma once

#include <string>
#include <vector>
#include <map>

#include <iostream>
#include <iomanip>  // setw()
//#include <cctype>   // 
#include <conio.h>  // _getch()

using namespace std;

class ATM_UI
{
public:
    ATM_UI() {};

    static void showHello(const string& bank_name);
    static void showGoodbye();
    static void showLine();

    static int showChoiseMenu(
        const vector<string>& options,
        const string& title = "",
        const string& enterMsg = "Make your choise",
        const bool showLines = true
    );

    static void waitForEnter();

    static void showMessage(const string& msg, bool wait=true);
    static void showInstruction(const string& msg);

    static void showCardInfo(string bank, string num, bool blockState);
    static void showCardBalance(const double balance);
    static void showCashboxInfo(int billsCount, map<int, int> bills);

    static int enterPIN();

    static int enterNumber(int max, string msg = "");
    static bool enterTrueFalse(string msg="");

protected:
    static string formatCardNumber(const string& n);
};
