#include <windows.h>
#include <iostream>
using namespace std;

// Длина массива, задана вариантом
const int N = 3200;

// Функция сортировки массива методом пузырька
void SortIntArr(int mas[N]) {
	int change;
	for (int i = 0; i < N - 1; i++) {
		for (int j = 0; j < N - i - 1; j++) {
			if (mas[j] > mas [j + 1]) {
				change = mas[j + 1];
				mas[j + 1] = mas[j];
				mas[j] = change;
			}
		}
	}
	return;
}

int main() {
	
	// Переменные для хранения времени
	SYSTEMTIME Tsrt, t1, t2, Tend;	
	
	// Время начала выполнения программы
	GetSystemTime(&Tsrt);
	cout << "Start time: ";
	cout << Tsrt.wMinute << ":" << Tsrt.wSecond << ":" << Tsrt.wMilliseconds << '\n';
	
	// Время начала выполнения сортировок
	GetSystemTime(&t1);
	
	int arr[N];
	
	// Заполнение массива случайными значениями и его сортировка (100 повторов)
	for (int j = 0; j < 100; j++) {
		for (int i = 0; i < N; i++) {
			arr[i] = rand() % 10000;
		}
		SortIntArr(arr);
	}
	
	// Время окончания цикла сортировок
	GetSystemTime(&t2);
	cout << "After sort: ";
	cout << t2.wMinute << ":" << t2.wSecond << ":" << t2.wMilliseconds << '\n';
	
	// Перевод t1 и t2 в 64-битовый формат 
	FILETIME ft1, ft2;
	ULARGE_INTEGER li1, li2, delta;
	SystemTimeToFileTime(&t1, &ft1);
	SystemTimeToFileTime(&t2, &ft2);
	li1.u.LowPart = ft1.dwLowDateTime;
	li1.u.HighPart = ft1.dwHighDateTime;
	li2.u.LowPart = ft2.dwLowDateTime;
	li2.u.HighPart = ft2.dwHighDateTime;
	
	// Поиск среднего времени одной сортировки в мсек. (t2-t1)/100
	delta.QuadPart = (li2.QuadPart - li1.QuadPart) / 100;
	cout << "Average time of one sort - " << delta.QuadPart / 10000 << " ms.\n";
	
	// Время окончания выполнения программы
	GetSystemTime(&Tend);
	cout << "End time: ";
	cout << Tend.wMinute << ":" << Tend.wSecond << ":" << Tend.wMilliseconds << '\n';
	
	system("pause");
	return 0;
}