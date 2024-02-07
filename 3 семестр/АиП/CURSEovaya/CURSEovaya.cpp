#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <conio.h>
#include <cmath>
#include <clocale>
using namespace std;

// КОНСТАНТЫ (клавиши)
const int Enter = 13;
const int Up = 72;
const int Down = 80;
const int Left = 75;
const int Right = 77;
const int Esq = 27;

// КОНСТАНТЫ (таблица)
string tabline = " _________________________________________________________________________________________________________________\n";
string tabhead = " | № |                ФИО студента                | Зачётка | Группа | Дата рождения | Год поступ. | Вступ. балл |\n";
string tabempt = " |   |                                            |         |        |               |             |             |\n";

// Структура для дат
struct Date
{
	unsigned short day;		// число
	unsigned short month;	// месяц
	unsigned short year;	// год
};

// Структура ФИО студента
struct Initial
{
	string surname;		// фамилия
	string name;		// имя
	string patronym;	// отчество
};

// Структура записи о студенте
struct Student
{
	int num;					// номер записи в таблице
	unsigned int record_num;	// номер зачётной книжки
	Initial FIO;				// имя
	string group;				// шифр группы
	Date birth;					// дата рождения
	unsigned short entry_year;	// год поступления
	unsigned short entry_score;	// вступительный балл
};

// Структура для списка
struct List
{
	struct Student inf;	// инф. поле
	struct List* prev;	// пред. элемент
	struct List* next;	// след. элемент
};

// Структура списка комманд
struct DirList
{
	int num;				// номер команды
	struct DirList* prev;	// пред команда
	struct DirList* next;	// след. команда
};

// Списки с номерами команд
DirList* choise1 = NULL;
DirList* choise2 = NULL;

// Флаг сохранённости списка
bool saved = false;

// Прототипы функций
List* createList(List* head);			// организация списка
Student fillStudentNote();				// заполнение элемента списка
void printList(List* head, List* cur);	// просмотр списка
List* printNote(List* note, List* cur);	// вывод элемента списка
List* deleteNote(List* head, List*cur);	// удаление записи
void editNote(List* cur);				// перезапись записи
List* sortList(List* head);				// сортировка списка
List* searchList(List* head, List*cur);	// поиск по списку
void saveToFile(List* head);			// выгрузка в файл
List* loadFromFile(List* head);			// загрузка из файла
List* cleanMemory(List* head);			// очищение памяти (таблица)
DirList* cleanMemoryDir(DirList* head);	// очищение памяти (команды)
List* tableMenuEsq(List* head);			// выход из основного меню
List* getLastNote(List* head);			// поиск последнего элемента
void searchBest(List* head);			// вывод лучших студентов по годам

// Заполнение списка команд в соответствии с переданным массивом
void fillCommArr(int comm[], int sizeArr, bool thr)
{
	DirList* choise = new DirList;
	choise->num = comm[0];
	DirList* dir = choise;
	for (int i = 1; i < sizeArr; i++)
	{
		DirList* newDir = new DirList;
		newDir->num = comm[i];
		newDir->prev = dir;
		dir->next = newDir;
		dir = dir->next;
	}
	dir->next = choise;
	choise->prev = dir;
	thr ? cleanMemoryDir(choise1) : cleanMemoryDir(choise2);
	thr ? (choise1 = choise) : (choise2 = choise);
}

// Выбор команды из предложенных вариантов
int selectCommand(int comm[], int sizeArr, bool thr)
{
	DirList* choise = thr ? (choise1) : (choise2);
	for (int i = 0; i < sizeArr; i++)
	{
		if (choise->num == comm[i]) cout << " > ";
		else cout << "   ";
		switch (comm[i])
		{
			case 1: cout << "Добавить запись \n"; break;
			case 2: cout << "Вывести список \n"; break;
			case 3: cout << "Удалить запись \n"; break;
			case 4: cout << "Сохранить список в файл \n"; break;
			case 5: cout << "Загрузить список из файла \n"; break;
			case 6: cout << "Создать новый список \n"; break;
			case 7: cout << "Продолжить ввод \n"; break;
			case 8: cout << "Завершить ввод \n"; break;
			case 9: cout << "Сортировать по имени\n"; break;
			case 10: cout << "Редактировать запись \n"; break;
			case 11: cout << "Отмена \n"; break;
			case 12: cout << "ОК \n"; break;
			case 13: cout << "Сортировать по возрастанию [^] \n"; break;
			case 14: cout << "Сортировать по убыванию    [v] \n"; break;
			case 15: cout << "Поиск внутри списка \n"; break;
			case 16: cout << "Лучшие студенты \n"; break;
			case 17: cout << "Выйти без сохранения \n"; break;
			case 18: cout << "Изменить имя \n"; break;
			case 19: cout << "Изменить номер зач. книжки \n"; break;
			case 20: cout << "Изменить группу \n"; break;
			case 21: cout << "Изменить дату рождения \n"; break;
			case 22: cout << "Изменить год поступления \n"; break;
			case 23: cout << "Изменить вступительный балл \n"; break;
			case 24: cout << "Перезаписать все поля \n"; break;
			case 0: cout << "Завершить работу \n"; break;
		}
	}
	char c = 0;
	while ((c != Up) && (c != Down) && (c != Enter) && (c != Left) && (c != Right) && (c != Esq))
		c = _getch();
	switch (c)
	{
		case Up: choise = choise->prev; break;
		case Down: choise = choise->next; break;
		case Enter: return choise->num; break;
		case Left: return Left; break;
		case Right: return Right; break;
		case Esq: return Esq; break;
	}
	thr ? (choise1 = choise) : (choise2 = choise);
	return - 1;
}

// Меню выбора команды
List* startMenu(List *head)
{
	int arr[] = { 6, 5, 0 };
	fillCommArr(arr, 3, 1);
	while (1)
	{
		system("cls");
		cout << " Программа обработки данных о студентах\n";
		cout << " Работа Мовенко Константина, ИС/б-21-2-о \n";
		cout << " Севастопольский государственный университет, 2022\n";
		cout << "--------------------------------------------------------------------\n";
		cout << " [^][v] - переключение команд  [Esq] - выход из программы \n";
		cout << "--------------------------------------------------------------------\n";
		cout << "\n   Выберите действие\n\n";
		switch (selectCommand(arr, 3, 1))
		{
		case 6:		// создание нового списка
			head = createList(head);
			return head;
			break;
		case 5:		// загрузка списка из файла
			head = loadFromFile(head);
			if (head) return head;
			break;
		case Esq: case 0:	// завершение программы
			head = cleanMemory(head);
			choise1 = cleanMemoryDir(choise1);
			choise2 = cleanMemoryDir(choise2);
			exit(0);
		default: break;
		}
	}
}

// Вывод списка и выбор команды по его обработке
List* tableMenu(List* head)
{
	List* cur = head;
	int arr[] = { 1, 10, 3, 9, 4, 15, 16 };
	fillCommArr(arr, 7, 1);
	while (1)
	{
		system("cls");
		printList(head, cur);
		switch (selectCommand(arr, 7, 1))
		{
		case 1:						// добавление элемента
			head = createList(head);
			cur = getLastNote(head);
			if (!cur) cur = head; break;
		case 10:					// перезапись элемента
			editNote(cur);
			break;
		case 3:						// удаление элемента
			if (cur) cur = deleteNote(head, cur);
			if (!cur) head = NULL;
			else if (cur->inf.num == 1) head = cur;
			break;
		case 9:						// сортировка по имени
			head = sortList(head);
			break;
		case 4:						// сохранение в файл
			saveToFile(head);
			break;
		case 15:					// поиск в списке
			cur = searchList(head, cur);
			break;
		case 16:					// вывод лучших
			searchBest(head);
			break;
		case 11:					// конец работы со списком
		case Esq:
			head = tableMenuEsq(head);
			if (saved) return NULL;
			break;
		// Перемещение по списку
		case Right: if (cur) if (cur->next) cur = cur->next; break;
		case Left: if (cur) if (cur->prev) cur = cur->prev; break;
		}
	}
}

// Выход из основного меню работы со списком
List* tableMenuEsq(List* head)
{
	if (!saved)
	{
		int arr[] = { 11, 17 };
		fillCommArr(arr, 2, 0);
		while (1)	// выбор действия
		{
			system("cls");
			cout << "\n  Изменения не сохранены. При выходе из списка данные не сохранятся.";
			cout << "\n\n  Выйти из списка? \n\n";
			int ask = selectCommand(arr, 2, 0);
			if (ask == 11) return head;
			if (ask == 17) break;
		}
	}
	head = cleanMemory(head);
	choise1 = cleanMemoryDir(choise1);
	saved = true;
	return head;
}

// НАЧАЛО ПРОГРАММЫ
int main() {
	setlocale(LC_ALL, "");
	List* head = NULL;
	while (1) {
		head = startMenu(head);	// начальное меню
		head = tableMenu(head);	// полный список комманд
	}
}

// Возвращает указатель на конец списка
List* getLastNote(List* head)
{
	if (!head) return head;
	while (head->next)
		head = head->next;
	return head;
}

// Ввод полож. целого числа с проверкой
int getInt(string mass, int max)
{
	long int x;
	string str;
	while (1)
	{
		cout << "  " << mass << " - ";
		getline(cin, str);
		int i = 0;
		if (!str.empty())
		{
			while (i < str.size())
			{
				if (!isdigit((unsigned char) str[i])) break;
				i++;
			}
		}
		if ((str.find(" ") < string::npos) || str.empty() || (i < str.size()))
		{
			cout << "\n  ОШИБКА: Некорректный ввод данных\n\n";
			continue;
		}
		if ((str.size() > to_string(max).size()) || ((x = stoi(str)) > max))
		{
			cout << "\n  ОШИБКА: Значение превышает " << max << "\n\n";
			continue;
		}
		break;
	}
	return x;
}

// Ввод строки без пробела
string getStr(string mass, int max)
{
	string str;
	while (1)
	{
		cout << "  " << mass << " - ";
		getline(cin, str);
		if ((str.find(" ") >= string::npos) && !str.empty())
			if (str.size() <= max) break;
			else
				cout << "\n  ОШИБКА: Чрезмерно длинное имя\n\n";
		else
			cout << "\n  ОШИБКА: Некорректный ввод данных\n\n";
	}
	return str;
}

// Заполнение информационного поля
Student fillStudentNote()
{
	Student stud;
	stud.num = 0;
	while (1)
	{		
		stud.FIO.surname = getStr("Фамилия", 38);
		stud.FIO.name = getStr("Имя", 38);
		stud.FIO.patronym = getStr("Отчество", 38);
		string f = stud.FIO.surname + " " + stud.FIO.name + " " + stud.FIO.patronym;
		if (f.length() <= 42) break;
		else cout << "\n  ОШИБКА: Чрезмерно длинное имя\n\n";
	}
	stud.record_num = getInt("Номер зачётной книжки (7 цифр)", 9999999);
	stud.group = getStr("Шифр группы (6 символов)", 6);
	stud.birth.day = getInt("Дата рождения (день)", 31);
	stud.birth.month = getInt("Месяц рождения", 12);
	stud.birth.year = getInt("Год рождения", 9999);
	stud.entry_year = getInt("Год поступления", 9999);
	stud.entry_score = getInt("Вступительный балл", 999);
	return stud;
}

// Присоединение элемента к списку
List* addNote(List* head, Student info)
{
	if (!head)	// создание головы списка
	{
		head = new List;
		head->inf = info;
		head->inf.num = 1;
		head->next = NULL;
		head->prev = NULL;
	}
	else	// добавление элемента в конец
	{
		List* newNote = new List;
		List* lastNote = getLastNote(head);
		newNote->inf = info;
		newNote->inf.num = lastNote->inf.num + 1;
		lastNote->next = newNote;
		newNote->next = NULL;
		newNote->prev = lastNote;
	}
	return head;
}

// Организация списка
List* createList(List* head)
{
	while (1)
	{
		system("cls");
		cout << "\n  Заполнение таблицы \n\n";
		Student info = fillStudentNote();
		head = addNote(head, info);
		saved = false;
		int arr[] = { 7, 8 };
		fillCommArr(arr, 2, 0);
		while (1)	// выбор действия
		{
			system("cls");
			cout << "\n   Выберите действие: \n\n";
			int ask = selectCommand(arr, 2, 0);
			if (ask == 8) return head;
			if (ask == 7) break;
		}
	}
}

// Перевод даты в строку
string printDate(Date date)
{
	string str;
	if (date.day > 9)
		str = to_string(date.day) + '.';
	else str = '0' + to_string(date.day) + '.';
	if (date.month > 9)
		str += to_string(date.month) + '.';
	else str += '0' + to_string(date.month) + '.';
	str += to_string(date.year);
	return str;
}

// Вывод элемента списка
List* printNote(List* note, List* cur)
{
	if (note)
	{
		cout << ((cur) && (note->inf.num == cur->inf.num) ? (">") : (" ")) << "|" << setw(3) << note->inf.num;
		string fullName = note->inf.FIO.surname + " " + note->inf.FIO.name + " " + note->inf.FIO.patronym;
		cout << "|" << setw(43) << fullName;
		cout << " |" << setw(8) << note->inf.record_num;
		cout << " |" << setw(7) << note->inf.group << " | ";
		cout << setw(14) << left << printDate(note->inf.birth);
		cout << "|" << right << setw(12) << note->inf.entry_year;
		cout << " |" << setw(12) << note->inf.entry_score << " |\n";
		cout << tabline;
		return note->next;
	}
	else
		cout << tabempt << tabline;
	return note;
}

// Поиск позиции (не индекса) элемента в списке
int findNotePos(List* head, List* cur)
{
	List* note = head;
	int pos = 1;
	while ((note) && (note->inf.num != cur->inf.num))
	{
		pos++;
		note = note->next;
	}
	return pos;
}

// Вывод списка
void printList(List* head, List* cur)
{
	int pos = findNotePos(head, cur);	// выбор страницы списка
	List* printHead = head;
	for (int i = 1; i < ceil((pos / 8.0)); i++)
	{
		printHead = printHead->next->next->next->next->next->next->next->next;
	}
	cout << tabline << tabhead << tabline;	// вывод списка в виде таблицы
	List* note = printHead;
	for (int i = 1; i <= 8; i++)
	{
		note = printNote(note, cur);
	}
	List* lastNote = getLastNote(head);
	int lNum = findNotePos(head, lastNote);
	string page = "Страница " + to_string((int)(ceil(pos / 8.0)));
	page += " / " + to_string((int)(ceil(lNum / 8.0)));
	cout << " |  " << setw(18) << left << page << right << setw(93) << "[Esq] - выйти  [<] [>] - список  [^] [v] - команды  |\n";
	cout << tabline << endl;
}

// Удаление элемента
List* deleteNote(List* head, List* del)
{
	int arr[] = { 11, 12 };
	fillCommArr(arr, 2, 0);
	int comCode = -1;
	while (comCode < 0)
	{
		system("cls");
		cout << "\n  Удалить запись? \n\n";
		switch (comCode = selectCommand(arr, 2, 0))
		{
			case 11: return del;
			case 12: break;
		}
	}
	saved = false;
	if (del->next) del->next->prev = del->prev;
	if (del->prev) del->prev->next = del->next;
	List* newcur = del->next;
	while (newcur)
	{
		newcur->inf.num--;
		newcur = newcur->next;
	}
	if (del->prev) newcur = del->prev;
	else newcur = del->next;
	delete del;
	return newcur;
}

// Перезапись элемента
void rewriteNote(List* cur)
{
	system("cls");
	cout << "\n  Перезапись элемента: \n\n";
	if (cur)
	{
		cur->inf = fillStudentNote();
		if (cur->prev) cur->inf.num = cur->prev->inf.num + 1;
		else cur->inf.num = 1;
		saved = false;
	}
	return;
}

// Редактирование элемента списка
void editNote(List* cur)
{
	if (!cur) return;
	int arr[] = { 18, 19, 20, 21, 22, 23, 24 };
	fillCommArr(arr, 7, 0);
	while (1)
	{
		system("cls");
		cout << tabline << tabhead << tabline;
		printNote(cur, NULL);
		cout << "\n  Редактирование элемента: \n";
		cout << "\n  Выйти - [Esq] \n\n";
		int com = selectCommand(arr, 7, 0);
		cout << endl;
		switch (com)
		{
			case 18:
				while (1)
				{
					cur->inf.FIO.surname = getStr("Фамилия", 38);
					cur->inf.FIO.name = getStr("Имя", 38);
					cur->inf.FIO.patronym = getStr("Отчество", 38);
					string f = cur->inf.FIO.surname + " " + cur->inf.FIO.name + " " + cur->inf.FIO.patronym;
					saved = false;
					if (f.length() <= 42) break;
					else cout << "\n  ОШИБКА: Чрезмерно длинное имя \n\n";
				}
				break;
			case 19:
				cur->inf.record_num = getInt("Номер зачётной книжки (7 цифр)", 9999999);
				saved = false;
				break;
			case 20:
				cur->inf.group = getStr("Шифр группы (6 символов)", 6);
				saved = false;
				break;
			case 21:
				cur->inf.birth.day = getInt("Дата рождения (день)", 31);
				cur->inf.birth.month = getInt("Месяц рождения", 12);
				cur->inf.birth.year = getInt("Год рождения", 9999);
				saved = false;
				break;
			case 22:
				cur->inf.entry_year = getInt("Год поступления", 9999);
				saved = false;
				break;
			case 23:
				cur->inf.entry_score = getInt("Вступительный балл", 999);
				saved = false;
				break;
			case 24:
				rewriteNote(cur);
				break;
			case Esq: return;
		}
	}
}

// Сравнение по ФИО
int initcmp(Initial n1, Initial n2)
{
	string name1 = n1.surname + " " + n1.name + " " + n1.patronym;
	string name2 = n2.surname + " " + n2.name + " " + n2.patronym;
	if (name1 > name2) return -1;
	if (name1 < name2) return 1;
	return 0;
}

// Сортировка списка по возрастанию
List* sortListAscend(List* head)
{
	List* il = getLastNote(head);
	while (il->prev)
	{
		List* jl = il->prev;
		while (jl)
		{
			if (initcmp(jl->inf.FIO, il->inf.FIO) < 0)
			{
				Student swap = il->inf;
				il->inf = jl->inf;
				jl->inf = swap;
				jl->inf.num = il->inf.num;
				il->inf.num = swap.num;
			}
			jl = jl->prev;
		}
		il = il->prev;
	}
	return head;
}

// Сорировка списка по убыванию
List* sortListDescend(List* head)
{
	List* il = getLastNote(head);
	while (il->prev)
	{
		List* jl = il->prev;
		while (jl)
		{
			if (initcmp(jl->inf.FIO, il->inf.FIO) > 0)
			{
				Student swap = il->inf;
				il->inf = jl->inf;
				jl->inf = swap;
				jl->inf.num = il->inf.num;
				il->inf.num = swap.num;
			}
			jl = jl->prev;
		}
		il = il->prev;
	}
	return head;
}

// Сортировка списка
List* sortList(List* head)
{
	if ((!head) || (!head->next)) return head;
	int arr[] = { 13, 14 };
	fillCommArr(arr, 2, 0);
	while (1)
	{
		system("cls");
		cout << "\n   Выберите сортировку: \n\n";
		cout << "  [Esq] - вернуться к списку\n\n";
		int ask = selectCommand(arr, 2, 0);
		if (ask == 13)
		{
			head = sortListAscend(head);
			saved = false;
			return head;
		}
		if (ask == 14)
		{
			head = sortListDescend(head);
			saved = false;
			return head;
		}
		if (ask == Esq) return head;
	}
	
}

// Проверка элемента на соответствие поиску
bool isSearched(List* el, string srch)
{
	if (!el) return false;
	string s;
	s = to_string(el->inf.num);							// по инексу
	if (s.find(srch) < string::npos) return true;
	s = el->inf.FIO.surname + " " + el->inf.FIO.name;	// по ФИО
	s += " " + el->inf.FIO.patronym;
	if (s.find(srch) < string::npos) return true;
	s = el->inf.group;									// по группе
	if (s.find(srch) < string::npos) return true;	
	s = to_string(el->inf.record_num);					// по зачётке
	if (s.find(srch) < string::npos) return true;
	s = printDate(el->inf.birth);						// по дате
	if (s.find(srch) < string::npos) return true;
	s = to_string(el->inf.entry_score);					// по баллу
	if (s.find(srch) < string::npos) return true;
	s = to_string(el->inf.entry_year);					// по году п.
	if (s.find(srch) < string::npos) return true;
	return false;
}

// Поиск внутри списка
List* searchList(List* head, List* cur)
{
	system("cls");
	string srch;
	if (!head) return head;
	while (1)	// ввод запроса
	{
		cout << "\n  Что искать - ";
		getline(cin, srch);
		if (!srch.empty()) break;
		else cout << endl;
	}
	List* shead = NULL;	// заполнение списка результатов
	List* run = head;
	while (run)
	{
		if (isSearched(run, srch))
		{
			shead = addNote(shead, run->inf);
			List* lastNote = getLastNote(shead);
			lastNote->inf.num = run->inf.num;
		}
		run = run->next;
	}
	if (!shead)		// результатов не найдено
	{
		cout << "\n  Не найдено результатов по запросу \n\n";
		system("pause");
		return cur;
	}
	run = shead;	// вывод результатов
	while (1)
	{
		system("cls");
		cout << "\n  Результаты по запросу [" << srch << "]: \n";
		printList(shead, run);
		cout << " > Перейти к элементу \n";
		char c = 0;
		while ((c != Right) && (c != Left) && (c != Esq) && (c != Enter))
			c = _getch();
		if ((c == Right) && run) if (run->next) run = run->next;
		if ((c == Left) && run) if (run->prev) run = run->prev;
		if (c == Esq) return cur;
		if (c == Enter) break;
	}
	cur = head;
	while (cur->inf.num != run->inf.num)
		cur = cur->next;
	shead = cleanMemory(shead);
	return cur;
}

// Сортировка целочисленного массива по возрастанию
void sortInt(int arr[], int len)
{
	for (int i = 1; i < len; i++)
		for (int j = 0; j < (len - i); j++)
		{
			if (arr[j] > arr[j + 1])
			{
				int swap = arr[j + 1];
				arr[j + 1] = arr[j];
				arr[j] = swap;
			}
		}
	return;
}

// Заполнение массива годов поступления
int fillEntryYearsArr(int years[], List* head)
{
	int len = 0;
	List* run = head;
	while (run)
	{
		bool hmm = true;
		for (int i = 0; i < len; i++)
			if (years[i] == run->inf.entry_year)
				hmm = false;
		if (hmm)
		{
			years[len] = run->inf.entry_year;
			len++;
		}
		run = run->next;
	}
	return len;
}

// Сортировка списка по убыванию оценки
List* sortBestList(List* head)
{
	if ((!head) || (!head->next)) return head;
	List* il = getLastNote(head);
	while (il->prev)
	{
		List* jl = il->prev;
		while (jl)
		{
			if (jl->inf.entry_score < il->inf.entry_score)
			{
				Student swap = il->inf;
				il->inf = jl->inf;
				jl->inf = swap;
				jl->inf.num = il->inf.num;
				il->inf.num = swap.num;
			}
			jl = jl->prev;
		}
		il = il->prev;
	}
	return head;
}

// Заполнить список 5 лучших студентов за год
List* bestForYear(List* head, int year)
{
	List* shead = NULL;
	List* run = head;
	int count = 0;
	while (run)
	{
		if (run->inf.entry_year == year)
		{
			shead = addNote(shead, run->inf);
			List* lastNote = getLastNote(shead);
			lastNote->inf.num = run->inf.num;
			count++;
		}
		run = run->next;
	}
	shead = sortBestList(shead);
	if (count > 5)
	{
		List* last = shead->next->next->next->next;
		List* del = last->next;
		last->next = NULL;
		del = cleanMemory(del);
	}
	return shead;
}

// Вывод списка лучших
void printBestList(List* shead, int y, int years[], int len)
{
	cout << tabline << tabhead << tabline;
	for (int i = 0; i < 5; i++)
		shead = printNote(shead, NULL);
	string str1 = "Год - " + to_string(years[y]);
	string str2 = "[Esq] - Выйти";
	if (y < (len - 1))
		str2 = "[>] - " + to_string(years[y + 1]) + "  " + str2;
	if (y > 0)
		str2 = "[<] - " + to_string(years[y - 1]) + "  " + str2;
	cout << " |  " << setw(18) << left << str1 << right << setw(90) << str2 << " | \n";
	cout << tabline << endl;
	return;
}

// Сохранение лучших в файл
void saveBestList(List* head, int years[], int len)
{
	List* full = bestForYear(head, years[0]);
	for (int i = 1; i < len; i++)
	{
		List* shead = bestForYear(head, years[i]);
		List* last = getLastNote(full);
		last->next = shead;
		shead->prev = last;
	}
	saveToFile(full);
	return;
}

// Поиск лучших студентов по годам
void searchBest(List* head)
{
	if (!head) return;
	int years[1000];
	int len = fillEntryYearsArr(years, head);
	sortInt(years, len);
	int y = 0;
	while (1)
	{
		system("cls");
		cout << "\n Лучшие студенты по годам: \n";
		List* shead = bestForYear(head, years[y]);
		printBestList(shead, y, years, len);
		cout << "\n > Сохранить в файл";
		shead = cleanMemory(shead);
		char c = 0;
		while ((c != Right) && (c != Left) && (c != Esq) && (c != Enter))
			c = _getch();
		if (c == Right) if (y < (len - 1)) y++;
		if (c == Left) if (y > 0) y--;
		if (c == Enter) saveBestList(head, years, len);
		if (c == Esq) break;
	}
	return;
}

// Сохранение списка в текстовый файл
void saveToFileTxt(List* head, string fileName)
{
	ofstream fout(fileName, ios::out);	// открытие потока
	if (!fout)
	{
		cout << "\n  Ошибка открытия файла \n\n";
		system("pause");
		return;
	}
	while (head)
	{
		fout << head->inf.FIO.surname << " ";
		fout << head->inf.FIO.name << " ";
		fout << head->inf.FIO.patronym << " ";
		fout << head->inf.record_num << " ";
		fout << head->inf.group << " ";
		fout << head->inf.birth.day << " ";
		fout << head->inf.birth.month << " ";
		fout << head->inf.birth.year << " ";
		fout << head->inf.entry_year << " ";
		fout << head->inf.entry_score << endl;
		head = head->next;
	}
	fout.close();
	saved = true;
	cout << "\n  Успешно сохранено \n\n  ";
	return;
}

// Сохранение списка в типизированный файл
void saveToFileDat(List* head, string fileName)
{
	ofstream f(fileName, ios::binary | ios::out);	// открытие потока
	if (!f)
	{
		cout << "\n  Ошибка открытия файла \n\n";
		return;
	}
	while (head)
	{
		size_t len;

		len = head->inf.FIO.surname.length() + 1;
		f.write((char*)&len, sizeof(len));
		f.write((char*)head->inf.FIO.surname.c_str(), len);

		len = head->inf.FIO.name.length() + 1;
		f.write((char*)&len, sizeof(len));
		f.write((char*)head->inf.FIO.name.c_str(), len);

		len = head->inf.FIO.patronym.length() + 1;
		f.write((char*)&len, sizeof(len));
		f.write((char*)head->inf.FIO.patronym.c_str(), len);

		f.write((char*)&head->inf.record_num, sizeof(head->inf.record_num));

		len = head->inf.group.length() + 1;
		f.write((char*)&len, sizeof(len));
		f.write((char*)head->inf.group.c_str(), len);

		f.write((char*)&head->inf.birth.day, sizeof(head->inf.birth.day));
		f.write((char*)&head->inf.birth.month, sizeof(head->inf.birth.month));
		f.write((char*)&head->inf.birth.year, sizeof(head->inf.birth.year));

		f.write((char*)&head->inf.entry_year, sizeof(head->inf.entry_year));
		f.write((char*)&head->inf.entry_score, sizeof(head->inf.entry_score));
		
		head = head->next;
	}
	f.close();
	saved = true;
	cout << "\n  Успешно сохранено \n\n  ";
	return;
}

// Сохранение списка в файл
void saveToFile(List* head)
{
	system("cls");
	string fileName;
	while (1)	// чтение имени файла
	{
		system("cls");
		cout << "\n  Введите название или адрес файла - ";
		getline(cin, fileName);
		if (fileName.empty()) continue;
		if (fileName.size() < 5)
		{
			cout << "\n  Ошибка: не достигнута минимальная длина имени файла \n\n  ";
			system("pause");
		}
		else break;
	}
	string type = fileName.substr(fileName.size() - 3);
	if (type == "txt")	// формат файла
		saveToFileTxt(head, fileName);
	else if ((type == "dat") || (type == "bin"))
		saveToFileDat(head, fileName);
	else
	{
		cout << "\n  Ошибка - не поддерживаемый формат файла";
		cout << "\n  Поддерживаемые форматы - txt, dat, bin\n\n ";
		system("pause");
	}
	system("pause");
	return;
}

// Чтение из текстового файла элемента списка
List* loadElementFromTxt(ifstream &f, List* t, List* l)
{
	t->inf.num = (l) ? (l->inf.num + 1) : 1;
	if (!f.eof()) f >> t->inf.FIO.surname; else return NULL;
	if (!f.eof()) f >> t->inf.FIO.name; else return NULL;
	if (!f.eof()) f >> t->inf.FIO.patronym; else return NULL;
	if (!f.eof()) f >> t->inf.record_num; else return NULL;
	if (!f.eof()) f >> t->inf.group; else return NULL;
	if (!f.eof()) f >> t->inf.birth.day; else return NULL;
	if (!f.eof()) f >> t->inf.birth.month; else return NULL;
	if (!f.eof()) f >> t->inf.birth.year; else return NULL;
	if (!f.eof()) f >> t->inf.entry_year; else return NULL;
	if (!f.eof()) f >> t->inf.entry_score; else return NULL;
	return t;
}

// Загрузка из текстового файла
List* loadFromFileTxt(string fileName)
{
	ifstream fin(fileName, ios::in);	// открытие потока
	if (!fin)
	{
		cout << "\n  Ошибка открытия файла \n\n";
		system("pause");
		return NULL;
	}
	List* head = NULL;	// чтение списка
	List* temp;
	while (1)
	{
		temp = new List;
		temp = loadElementFromTxt(fin, temp, getLastNote(head));
		if (!temp)
		{
			delete temp;
			fin.close();
			if (!head)	// файл пуст
			{
				cout << "\n  Ошибка: файл пустой \n\n";
				system("pause");
			}
			else saved = true;
			return head;
		}
		head = addNote(head, temp->inf);
		delete temp;
	}
}

// Чтение из файла элемента списка
List* loadElementFromBin(ifstream& f, List* t, List* l)
{
	if (f.eof()) return NULL;

	t->inf.num = (l) ? (l->inf.num + 1) : 1;

	try
	{
		size_t len;
		char* buf;
		f.read((char*)&len, sizeof(len));
		buf = new char[len];
		f.read(buf, len);
		t->inf.FIO.surname = buf;
		delete[] buf;
		buf = NULL;

		f.read((char*)&len, sizeof(len));
		buf = new char[len];
		f.read(buf, len);
		t->inf.FIO.name = buf;
		delete[] buf;
		buf = NULL;

		f.read((char*)&len, sizeof(len));
		buf = new char[len];
		f.read(buf, len);
		t->inf.FIO.patronym = buf;
		delete[] buf;
		buf = NULL;

		f.read((char*)&t->inf.record_num, sizeof(t->inf.record_num));

		f.read((char*)&len, sizeof(len));
		buf = new char[len];
		f.read(buf, len);
		t->inf.group = buf;
		delete[] buf;
		buf = NULL;

		f.read((char*)&t->inf.birth.day, sizeof(t->inf.birth.day));
		f.read((char*)&t->inf.birth.month, sizeof(t->inf.birth.month));
		f.read((char*)&t->inf.birth.year, sizeof(t->inf.birth.year));
		f.read((char*)&t->inf.entry_year, sizeof(t->inf.entry_year));
		f.read((char*)&t->inf.entry_score, sizeof(t->inf.entry_score));
	}
	catch (...)
	{
		return NULL;
	}
	return t; 
}

// Загрузка из бинарного файла
List* loadFromFileBin(string fileName)
{
	ifstream fin(fileName, ios::binary | ios::in);
	if (!fin)
	{
		cout << "\n  Ошибка открытия файла \n\n ";
		system("pause");
		return NULL;
	}

	List* head = NULL;	// чтение списка
	List* temp;
	while (1)
	{
		temp = new List;
		temp = loadElementFromBin(fin, temp, getLastNote(head));
		if (!temp)
		{
			fin.close();
			if (!head)	// файл пуст
			{
				cout << "\n  Ошибка: файл пустой \n\n ";
				system("pause");
			}
			else saved = true;
			return head;
		}
		head = addNote(head, temp->inf);
		delete temp;
	}
}

// Загрузка списка из файла
List* loadFromFile(List* head)
{
	head = cleanMemory(head);
	string fileName;
	while (1)	// чтение имени файла
	{
		system("cls");
		cout << "\n  Введите название или адрес файла - ";
		getline(cin, fileName);
		if (fileName.empty()) continue;
		if (fileName.size() < 5)
		{
			cout << "\n  Ошибка: не достигнута минимальная длина имени файла \n\n  ";
			system("pause");
		}
		else break;
	}
	string type = fileName.substr(fileName.size() - 3);
	if (type == "txt")	// формат файла
		head = loadFromFileTxt(fileName);
	else if ((type == "dat") || (type == "bin"))
		head = loadFromFileBin(fileName);
	else
	{
		cout << "\n  Ошибка - не поддерживаемый формат файла";
		cout << "\n  Поддерживаемые форматы - txt, dat, bin\n\n ";
		system("pause");
	}
	return head;
}

// Очищение памяти главного списка
List* cleanMemory(List* head)
{
	List* currNote;
	while (head)
	{
		currNote = head;
		head = head->next;
		delete currNote;
	}
	return head;
}

// Очищение памяти списка комманд
DirList* cleanMemoryDir(DirList* head)
{
	DirList* currNote;
	if (head && head->prev)
		 head->prev->next = NULL;
	while (head)
	{
		currNote = head;
		head = head->next;
		delete currNote;
	}
	return head;
}
