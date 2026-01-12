#include <iostream>
#include <string>
using namespace std;

// Абстрактное ОРУЖИЕ
class Weapon {
public:
	virtual void attack() = 0;
};

// МЕЧ (бить)
class Sword : public Weapon {
public:
    void attack() override  { cout << "Swinging the sword!\n"; }
};

// ЛУК (стрелять)
class Bow : public Weapon {
public:
    void attack() override { cout << "Shooting an arrow!\n"; }
};

// Абстрактная БРОНЯ
class Armor {
public:
	virtual void protect() = 0;
};

// ТЯЖЁЛАЯ БРОНЯ (Хавел)
class HeavyArmor : public Armor {
public:
    void protect() override { cout << "YOU SHALL NOT TOUCH ME \n"; }
};

// ЛЁГКАЯ БРОНЯ
class LightArmor : public Armor {
public:
    void protect() override { cout << "Fashion works badly at battle( \n"; }
};

// Персонаж (жёстко привязан к строкам)
class Character {
private:
    string type;
    Weapon* weapon = nullptr;
    Armor* armor = nullptr;

public:
    Character(Weapon* w, Armor* a) : weapon(w), armor(a) {}

    ~Character() {
        delete weapon;
        delete armor;
    }

    void attack() { weapon->attack(); }
    void protect() { armor->protect(); }
};

// Код программы
int main() {
    Character warrior(new Sword, new HeavyArmor);
    warrior.attack();
    warrior.protect();

	cout << "-------------\n";

    Character archer(new Bow, new LightArmor);
    archer.attack();
    archer.protect();

    return 0;
}

