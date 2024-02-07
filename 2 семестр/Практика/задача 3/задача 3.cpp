#include <iostream>
#include <string>
using namespace std;

//структура оценок студентов
typedef struct studentMarks {
    float physics;
    float history;
    float maths;
} studentMarks;

//структура информации о студенте
typedef struct student {
    int id;
    string lastname;
    studentMarks marks;
} student;

//структура списка (инф. поле и указатель на след. элемент)
typedef struct node {
    student el;
    node* next;
} node;

//структура указателя на список
typedef struct list {
    node* head;
    int size;
} list;

//прототипы функций
list* init();
node* get(list* l, int index);
void push(list* l, student el);
string marshal(student el);
student unmarshal(string s);
bool swapByLastname(list* l, string lastnameA, string lastnameB);

//главная функция
int main()
{
    list* MyList = init();
    student MyStudent;
    MyStudent.id = 3;
    MyStudent.lastname = "Petrov";
    MyStudent.marks.history = 1;
    MyStudent.marks.maths = 1;
    MyStudent.marks.physics = 1;
    push(MyList, MyStudent);
    MyStudent.id = 3;
    MyStudent.lastname = "Sidorov";
    MyStudent.marks.history = 2;
    MyStudent.marks.maths = 2;
    MyStudent.marks.physics = 2;
    push(MyList, MyStudent);
    MyStudent.id = 6;
    MyStudent.lastname = "Ivanov";
    MyStudent.marks.history = 3.0;
    MyStudent.marks.maths = 3.2;
    MyStudent.marks.physics = 3.3;
    push(MyList, MyStudent);
    node* a = new node;
    a = MyList->head;
    while (a != NULL) {
        cout << a->el.lastname << "\n";
        a = a->next;
    }
    node* g = get(MyList, 2);
    if (g != NULL) cout << "answer - " << g->el.lastname << "\n";
    string S = marshal(MyStudent);
    cout << S << "\n";
    MyStudent = unmarshal(S);
    cout << "answer - " << MyStudent.marks.physics << "\n";
    cout << swapByLastname(MyList, "Petrov", "Ivanov") << "\n";
    a = MyList->head;
    while (a != NULL) {
        cout << a->el.lastname << "\n";
        a = a->next;
    }
}

//инициализация пустого списка
list* init() {
    list* MyList = new list;
    MyList->head = NULL;
    MyList->size = 0;
    return MyList;
}

//получение студента из списка по индексу
node* get(list* l, int index) {
    int num = -1;
    node* t = l->head;
    while (t != NULL) {
        num++;
        if (num == index) return t;
        t = t->next;
    }
    return NULL;
}

//добавление студента в конец списка
void push(list* l, student el) {
    if (l->head == NULL) {
        l->head = new node;
        l->head->el = el;
        l->head->next = NULL;
        l->size++;
        return;
    }
    node* t = l->head;
    while (t->next != NULL)
        t = t->next;
    t->next = new node;
    t->next->el = el;
    t->next->next = NULL;
    l->size++;
    return;
}

//конвертирует переданную структуру в строку
string marshal(student el) {
    string Str = to_string(el.id) + " ";
    Str = Str + el.lastname + " ";
    string s = to_string(el.marks.physics);
    while ((s[s.length() - 1] == '0') || (s[s.length() - 1] == '.'))
        s = s.substr(0, s.length() - 1);
    Str = Str + s + " ";
    s = to_string(el.marks.history);
    while ((s[s.length() - 1] == '0') || (s[s.length() - 1] == '.'))
        s = s.substr(0, s.length() - 1);
    Str = Str + s + " ";
    s = to_string(el.marks.maths);
    while ((s[s.length() - 1] == '0') || (s[s.length() - 1] == '.'))
        s = s.substr(0, s.length() - 1);
    Str = Str + s;
    return Str;
}

//конвертирует строку marshal в структуру student
student unmarshal(string s) {
    student Student;
    string subS = "";
    int num = 0;
    for (int i = 0; i <= s.length(); i++)
        if ((s[i] == ' ') || (s[i] == '\0')) {
            num++;
            switch (num) {
            case 1: Student.id = stoi(subS); break;
            case 2: Student.lastname = subS; break;
            case 3: Student.marks.physics = stof(subS); break;
            case 4: Student.marks.history = stof(subS); break;
            case 5: Student.marks.maths = stof(subS); break;
            }
            subS.clear();
        }
        else subS = subS + s[i];
    return Student;
}

//меняет местами в списке студентов с заданными аргументами фамилиями
bool swapByLastname(list* l, string lastnameA, string lastnameB) {
    student exchange;
    node* nodeA = l->head;
    while (nodeA != NULL) {
        if (nodeA->el.lastname == lastnameA) break;
        nodeA = nodeA->next;
    }
    node* nodeB = l->head;
    while (nodeB != NULL) {
        if (nodeB->el.lastname == lastnameB) break;
        nodeB = nodeB->next;
    }
    if ((nodeA == NULL) || (nodeB == NULL))
        return false;
    exchange = nodeA->el;
    nodeA->el = nodeB->el;
    nodeB->el = exchange;
    return true;
}