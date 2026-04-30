#include <iostream>

#include "BankCard.h"
#include "Person.h"
#include "Client.h"
#include "ATM.h"

using namespace std;

int main()
{
    cout << "Hello World!" << endl;

    Client* man = new Client("Ivan Maheev");

    BankCard* card1 = new BankCard(123456, "NovaBank", man, 1234);
    BankCard* card2 = new BankCard(111111, "BangBank", man, 0000);
    BankCard* card3 = new BankCard(909090, "Platinum", man, 1111);

    man->addCard(card1);
    man->addCard(card2);
    man->addCard(card3);

    cout << "User " << man->getName() << " has cards: " << endl;
    for (int i = 0; i < man->getCards().size(); i++) {
        cout << "   Card" << i + 1 << ": " << man->getCards()[i]->getBank() << endl;
    }

    ATM* atm = new ATM("NovaBank");

    atm->startSession(man->getCards()[0]);
}
