#include "Person.h"

Person::Person(string name) {
	this->name = name;
}

/*void Person::startWorkWithATM(ATM atm) {

}*/

string Person::getName() {
	return this->name;
}
