#include <iostream>
#include <string>

using namespace std;

// Абстрактное ОРУЖИЕ
class Weapon {
public:
    virtual void attack() = 0;
    virtual ~Weapon() {}
};

// МЕЧ (бить)
class Sword : public Weapon {
public:
    void attack() override { cout << "Swinging the sword!\n"; }
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
    virtual ~Armor() {}
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

// абстрактная ФАБРИКА ПЕРСОНАЖЕЙ (звёзд)
class CharacterFactory {
public:
    virtual Weapon* createWeapon() = 0;
    virtual Armor*  createArmor() = 0;
};


// ФАБРИКА МЕЧНИКОВ
class WarriorFactory : public CharacterFactory {
public:
    Weapon* createWeapon() { return new Sword; };
    Armor*  createArmor() { return new HeavyArmor; };
};

// ФАБРИКА ЛУЧНИКОВ
class ArcherFactory : public CharacterFactory {
public:
    Weapon* createWeapon() { return new Bow; };
    Armor*  createArmor() { return new LightArmor; };
};

// ПЕРСОНАЖ!!!!!
class Character {
private:
    Weapon* weapon;
    Armor* armor;

public:
    Character(CharacterFactory* factory) {
    	weapon = factory->createWeapon();
    	armor = factory->createArmor();
	}
	
    ~Character() {
        delete weapon;
        delete armor;
    }

    void attack() { weapon->attack(); }
    void protect() { armor->protect(); }
};

// КОД ПРОГРАММЫ
int main() {
	// фабрики держатся на стеке
	WarriorFactory warriorData;
	ArcherFactory archerData;
	
    Character warrior(&warriorData);
    warrior.attack();
    warrior.protect();

    cout << "-------------\n";

    Character archer(&archerData);
    archer.attack();
    archer.protect();

    return 0;
}
