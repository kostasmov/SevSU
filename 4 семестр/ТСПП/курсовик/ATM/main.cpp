#include <iostream>
#include <vector>
#include <cstdlib>

#include "BankCard.h"
#include "Client.h"
#include "Collector.h"
#include "BankOfficer.h"
#include "ATM.h"

using namespace std;

// Задание пользователей
static vector<Person*> createUsers() {
    Client* client = new Client("Ivan Maheev");

    client->addCard(new BankCard("1234567891011121", "NovaBank", client, 1234));
    client->addCard(new BankCard("1122334455667788", "BangBank", client, 0000));
    client->addCard(new BankCard("9999000099990000", "Platinum", client, 1111));

    Collector* collector = new Collector("Mihail Ladogin", 1);
    BankOfficer* officer = new BankOfficer("Nina Baranova", 33);

    Client* client2 = new Client("Eduard Afrikanov");
    client2->addCard(new BankCard("1010101010101010", "NovaBank", client2, 4321));

    return vector<Person*>{ client, collector, officer, client2 };
}

// Выбор пользователя
static int chooseUser(vector<Person*> users) {
    cout << "Users list: " << endl;
    for (int i = 0; i < users.size(); i++) {
        cout << "   " << i + 1 << " - " << users[i]->getName();
        cout << " (" << users[i]->getRole() << ")" << endl;
    }

    cout << "   ----------------------------------" << endl;
    cout << "   0 - Exit programm" << endl;
    
    // запрашивать "код" пользователя
    int userIndex = -1;
    while (userIndex < 0 || userIndex > users.size()) {
        userIndex = ATM_UI::enterNumber(1, "Choose user or exit programm");
    }

    return userIndex - 1;
}

// Выбор карты
static int chooseBankCard(Client* user) {
    // вывести на экран имя клиента
    cout << "User's name - " << user->getName() << endl;
    
    int cardsAmount = int(user->getCards().size()); // количество карт у клиента
    if (cardsAmount == 0) return -1;

    // вывести список карт
    cout << "Cards: " << endl;
    for (int i = 0; i < cardsAmount; i++) {
        cout << "   " << i + 1 << " - " << user->getCards()[i]->getBank() << endl;
    }

    // запрашивать "код" карты
    int cardNum = 0;
    while (cardNum <= 0 || cardNum > cardsAmount) {
        cardNum = ATM_UI::enterNumber(2, "Choose card for operations");
    }

    return cardNum - 1;
}


// ============================ ВЫПОЛНЕНИЕ ПРОГРАММЫ ============================
int main()
{
    cout << "Hello World!" << "\n\n";

    vector<Person*> users = createUsers();

    // есть ОДИН банкомат (банк указан, но, УВЫ, не участвует в логике)
    ATM* atm = new ATM("NovaBank");
    
    while (true) {
        // выбрать пользователя (или выбрать "не выбирать")
        int code = chooseUser(users);

        // конец программф
        if (code < 0) {
            cout << "Goodbye World!" << "\n\n";
            break;
        }

        Person* user = users[code];
        string role = user->getRole();
        
        // ========== КЛИЕНТ ==========
        if (role == "client") {
            Client* client = dynamic_cast<Client*>(user);
            int cardIndex = chooseBankCard(client);

            // cеанс обслуживание клиента на банкомате
            atm->startSession(client, client->getCards()[cardIndex]);
        }

        // ========== ИНКАССАТОР ==========
        else if (role == "collector") {
            Collector* collector = dynamic_cast<Collector*>(user);
            
            //
            cout << "COLLECTOR'S SCENARIO NOT DONE\n\n";
            //
        }

        // ========== СОТРУДНИК БАНКА ==========
        else if (role == "officer") {
            BankOfficer* officer = dynamic_cast<BankOfficer*>(user);

            //
            cout << "OFFICER'S SCENARIO NOT DONE\n\n";
            //
        }

        ATM_UI::waitForEnter();
        system("cls");
    }

    // очистка памяти
    delete atm;
    for (Person* user : users) { delete user; }

    return 0;
}