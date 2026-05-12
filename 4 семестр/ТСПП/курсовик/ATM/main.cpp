#include "BankCard.h"
#include "Client.h"
#include "Collector.h"
#include "BankOfficer.h"
#include "ATM.h"

#include <iostream>
#include <vector>

using namespace std;

// ============================ ЗАПОЛНЕНИЕ ДАННЫХ ============================

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
    client2->getCards()[0]->deposit(900000);

    return vector<Person*>{ client, collector, officer, client2 };
}



// ========================== ВЫБОР ДАННЫХ/ОПЕРАЦИЙ ==========================

// Выбор пользователя
static Person* chooseUser(const vector<Person*>& users) {
    vector<string> userList;
    
    for (auto* user : users) {
        userList.push_back(user->getName() + " (" + user->getRole() + ")");
    }

    int userIndex = ATM_UI::showChoiseMenu(
        userList, "Users list", "Choose user", false
    );

    if (userIndex == 0) return nullptr;
    return users[userIndex - 1];
}

// Выбор карты
static BankCard* chooseBankCard(Client* user) {
    int cardsAmount = int(user->getCards().size()); // количество карт у клиента
    if (cardsAmount == 0) return nullptr;

    vector<string> cardsList;

    for (auto* card : user->getCards()) {
        cardsList.push_back(card->getBank());
    }

    int cardIndex = ATM_UI::showChoiseMenu(
        cardsList, 
        "Cards of " + user->getName(), 
        "Choose card for operations",
        false
    );

    if (cardIndex == 0) return nullptr;
    return user->getCards()[cardIndex - 1];
}



// =========================== ВЫПОЛНЕНИЕ ПРОГРАММЫ ===========================
int main()
{
    vector<Person*> users = createUsers();
    ATM* atm = new ATM("NovaBank");
    
    while (true) {
        system("cls");
        cout << "___Hello World!___" << endl;

        // выбрать пользователя
        Person* user = chooseUser(users);

        // если пользователь не выбран - конец программы
        if (!user) {
            cout << "\n___Goodbye World!___\n";
            break;
        }

        string role = user->getRole();
        
        // ============== КЛИЕНТ ==============
        if (role == "client") {
            Client* client = dynamic_cast<Client*>(user);

            BankCard* card = chooseBankCard(client);
            if (!card) continue;

            // cеанс обслуживание клиента на банкомате
            atm->startSession(client, card);
        }

        // ============ ИНКАССАТОР ============
        else if (role == "collector") {
            Collector* collector = dynamic_cast<Collector*>(user);
            
            atm->startSession(collector);
        }

        // ========== СОТРУДНИК БАНКА ==========
        else if (role == "officer") {
            BankOfficer* officer = dynamic_cast<BankOfficer*>(user);

            // -------
            cout << "\nOFFICER'S SCENARIO NOT DONE\n";
            // -------
        }

        ATM_UI::waitForEnter();
    }

    // очистка памяти
    delete atm;
    for (Person* user : users) { delete user; }

    return 0;
}