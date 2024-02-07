#include <iostream>
#include <string>
using namespace std;

//структура оценок студента
typedef struct studentMarks {
    float physics;
    float history;
    float maths;
} studentMarks;

//структура информ. поля студента
typedef struct student {
    int id;
    string lastname;
    studentMarks marks;
} student;

//структура дерева
typedef struct node {
    student el;
    node* left;
    node* right;
} node;

//прототипы функций
node* get(node* head, string lastname);
node* push(node* head, student el);
string printContent(node* head);
string printStruct(node* head, string prefix);
node* getWorstStudent(node* head);

void seeTree(node* head) {
    if (head == NULL) return;
    seeTree(head->left);
    cout << head->el.lastname << "\n";
    seeTree(head->right);
}

//главная функция
int main()
{
    node* treeHead = NULL;
    student MyStudent;
    MyStudent.id = 3;
    MyStudent.lastname = "Petrov";
    MyStudent.marks.history = 9.0;
    MyStudent.marks.maths = 9.7;
    MyStudent.marks.physics = 9.987;
    treeHead = push(treeHead, MyStudent);
    MyStudent.id = 6;
    MyStudent.lastname = "Sidorov";
    MyStudent.marks.history = 3;
    MyStudent.marks.maths = 3;
    MyStudent.marks.physics = 3;
    push(treeHead, MyStudent);
    MyStudent.id = 9;
    MyStudent.lastname = "Ivanov";
    MyStudent.marks.history = 4;
    MyStudent.marks.maths = 4;
    MyStudent.marks.physics = 4;
    push(treeHead, MyStudent);
    MyStudent.id = 0;
    MyStudent.lastname = "Alexandrov";
    MyStudent.marks.history = 5;
    MyStudent.marks.maths = 5;
    MyStudent.marks.physics = 5;
    push(treeHead, MyStudent);
    MyStudent.id = 12;
    MyStudent.lastname = "Nikitin";
    MyStudent.marks.history = 3;
    MyStudent.marks.maths = 3;
    MyStudent.marks.physics = 3;
    push(treeHead, MyStudent);
    seeTree(treeHead);
    node* g = get(treeHead, "Ivanov");
    if (g) cout << "answer - " << g->el.id << "\n";
    cout << printContent(treeHead);
    cout << printStruct(treeHead, "");
    g = getWorstStudent(treeHead);
    cout << "worst one is " << g->el.lastname;
}

//получение студента из дерева по ключу
node* get(node* head, string lastname) {
    if (!head) return NULL;
    if (head->el.lastname == lastname)
        return head;
    if (lastname < head->el.lastname)
        return get(head->left, lastname);
    else
        return get(head->right, lastname);
}

//добавление студента в дерево
node* push(node* head, student el) {
    if (!head) {
        head = new node;
        head->el = el;
        head->left = NULL;
        head->right = NULL;
        return head;
    }
    if (el.lastname <= head->el.lastname)
        head->left = push(head->left, el);
    else head->right = push(head->right, el);
    return head;
}

//перевод числа типа float в строку (обрезает лишние нули)
string floatCut(float mark) {
    string s = to_string(mark);
    while ((s[s.length() - 1] == '0') || (s[s.length() - 1] == '.'))
        s = s.substr(0, s.length() - 1);
    return s;
}

//конвертирует переданное дерево в строку с данными дерева
string printContent(node* head) {
    string s, StrTree = "";
    if (!head) return "";
    StrTree += printContent(head->left);
    StrTree += to_string(head->el.id) + " ";
    StrTree += head->el.lastname + " ";
    StrTree += floatCut(head->el.marks.physics) + " ";
    StrTree += floatCut(head->el.marks.history) + " ";
    StrTree += floatCut(head->el.marks.maths) + "\n";
    StrTree += printContent(head->right);
    return StrTree;
}

//конвертирует переданное дерево в строку, демонстрирующую структуру дерева
string printStruct(node* head, string prefix) {
    string s, StrStruct = "";
    if (!head) return "";
    StrStruct += printStruct(head->left, prefix + "\t");
    StrStruct += prefix + to_string(head->el.id) + " ";
    StrStruct += head->el.lastname + " ";
    StrStruct += floatCut(head->el.marks.physics) + " ";
    StrStruct += floatCut(head->el.marks.history) + " ";
    StrStruct += floatCut(head->el.marks.maths) + "\n";
    StrStruct += printStruct(head->right, prefix + "\t");
    return StrStruct;
}

//сравнение двух студентов
node* compare(node* A, node* B) {
    float mark1, mark2;
    mark1 = (A->el.marks.history + A->el.marks.maths + A->el.marks.physics) / 3;
    mark2 = (B->el.marks.history + B->el.marks.maths + B->el.marks.physics) / 3;
    return ((mark1 < mark2) ? A : B);
}

//определение студента с наименьшим средним баллом
node* getWorstStudent(node* head) {
    if (!head) return NULL;
    node* minNode = head;
    if (head->left)
        minNode = compare(minNode, getWorstStudent(head->left));
    if (head->right)
        minNode = compare(minNode, getWorstStudent(head->right));
    return minNode;
}