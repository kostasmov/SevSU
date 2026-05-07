#include <iostream>

#include "BankCard.h"
#include "Person.h"
#include "Client.h"
#include "ATM.h"

using namespace std;

// выбор карты
static int chooseBankCard(Client* user) {
    // вывести на экран имя клиента и список его карта
    cout << "User's name - " << user->getName() << endl;
    cout << "Cards: " << endl;

    int cardsAmount = int(user->getCards().size());
    int cardNum = 0;

    for (int i = 0; i < cardsAmount; i++) {
        cout << "   " << i + 1 << " - " << user->getCards()[i]->getBank() << endl;
    }

    while (cardNum <= 0 || cardNum >= cardsAmount + 1) {
        cardNum = ATM_UI::enterNumber(2, "Choose card for operations");
    }

    return cardNum - 1;
}

// ============================ ВЫПОЛНЕНИЕ ПРОГРАММЫ ============================
int main()
{
    cout << "Hello World!" << "\n\n";

    // Есть человек (клиент)
    Client* man = new Client("Ivan Maheev");
    Client* man = new Client("Ivan Maheev");

    // Есть разные карты разных банков
    BankCard* card1 = new BankCard("1234567891011121", "NovaBank", man, 1234);
    BankCard* card2 = new BankCard("1122334455667788", "BangBank", man, 0000);
    BankCard* card3 = new BankCard("9999000099990000", "Platinum", man, 1111);

    // Все карты принадлежат клиенту
    man->addCard(card1);
    man->addCard(card2);
    man->addCard(card3);

    int cardIndex = chooseBankCard(man);

    // Есть банкомат (банк указан, но, УВЫ, не участвует в логике)
    ATM* atm = new ATM("NovaBank");

    // Сеанс обслуживание клиента на банкомате
    atm->startSession(man, man->getCards()[cardIndex]);
}