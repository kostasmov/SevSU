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

// Класс КОНТРОЛЯ ДОСТУПА
class AccessController {
public:
	// проверка прав доступа при входе в здание
    static void enterSystem(User user) {
        cout << "Checking rights of " << user.getName() << "..." << endl;
        
        switch (user.getRole()) { 
			case UserRoles::GUEST: 
				cout << "Issuing guest pass..." << endl; 
				break; 
				
			case UserRoles::EMPLOYEE: 
				cout << "Checking employee ID..." << endl; 
				break; 
				
			case UserRoles::ADMIN: 
				cout << "Checking employee ID..." << endl; 
				cout << "Verifying admin access level..." << endl; 
				break; 
		}
        
		cout << "Access granted!" << endl << endl;
    }
};

// КОД ПРОГРАММЫ
int main() {
    User guest(UserRoles::GUEST, "Ivan");
    User employee(UserRoles::EMPLOYEE, "Maria");
    User admin(UserRoles::ADMIN, "Ruslan");

    AccessController::enterSystem(guest);
    AccessController::enterSystem(employee);
    AccessController::enterSystem(admin);

    return 0;
}