#include <iostream>
#include <string>

using namespace std;

// возможные роли пользователей
enum class UserRoles { GUEST, EMPLOYEE, ADMIN };

// Класс ПОЛЬЗОВАТЕЛЬ
class User {
    UserRoles role;	// роль пользователя
    string name;	// имя
    
public:
    User(UserRoles role, string name) : role(role), name(name) {}
    
    string getName() { return name; }
    UserRoles getRole() { return role; }
};

// Абстрактный КОНТРОЛЛЕР ДОСТУПА
class AccessController {
    AccessController* _successor = nullptr;   // преемник
    
public:
    AccessController(AccessController* s = nullptr) { _successor = s; }
    virtual ~AccessController() = default;
    
    virtual void enterSystem(User& user) {
        if (_successor) {
        	_successor->enterSystem(user);
		} else {
			cout << "--- Access denied ---" << endl << endl;
		}
    }
};

// Контроллер для ГОСТЕЙ
class GuestAccessController : public AccessController {
public:
	GuestAccessController(AccessController* s = nullptr) : AccessController(s) {}
	
    void enterSystem(User& user) override {
        if (user.getRole() == UserRoles::GUEST) {
            cout << "Checking rights of " << user.getName() << "..." << endl;
            cout << "Issuing guest pass..." << endl; 
            cout << "Access granted!" << endl << endl;
        } else {
            AccessController::enterSystem(user);
        }
    }
};

// Контроллер для СОТРУДНИКОВ
class EmployeeAccessController : public AccessController {
public:
	EmployeeAccessController(AccessController* s = nullptr) : AccessController(s) {}
	
    void enterSystem(User& user) override {
        if (user.getRole() == UserRoles::EMPLOYEE) {
            cout << "Checking rights of " << user.getName() << "..." << endl;
            cout << "Checking employee ID..." << endl; 
            cout << "Access granted!" << endl << endl;
        } else {
            AccessController::enterSystem(user);
        }
    }
};

// Контроллер для АДМИНИСТРАТОРОВ
class AdminAccessController : public AccessController {
public:
	AdminAccessController(AccessController* s = nullptr) : AccessController(s) {}
	
    void enterSystem(User& user) override {
        if (user.getRole() == UserRoles::ADMIN) {
            cout << "Checking rights of " << user.getName() << "..." << endl;
            cout << "Checking employee ID..." << endl; 
            cout << "Verifying admin access level..." << endl; 
            cout << "Access granted!" << endl << endl;
        } else {
            AccessController::enterSystem(user);
        }
    }
};

// КОД ПРОГРАММЫ
int main() {
    // цепочка указателей на обработчики
    AccessController* adminAccess = new AdminAccessController();
    AccessController* employeeAccess = new EmployeeAccessController(adminAccess);
    AccessController* guestAccess = new GuestAccessController(employeeAccess);

    // пользователи
    User guest(UserRoles::GUEST, "Ivan");
    User employee(UserRoles::EMPLOYEE, "Maria");
    User admin(UserRoles::ADMIN, "Ruslan");

    // запуск цепочки (GUEST->EMPLOYEE->ADMIN)
    guestAccess->enterSystem(guest);
    guestAccess->enterSystem(employee);
    guestAccess->enterSystem(admin);

    return 0;
}
