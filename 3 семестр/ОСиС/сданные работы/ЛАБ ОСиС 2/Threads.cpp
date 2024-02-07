#include <windows.h>
#include <iostream>
using namespace std;

// Длина массива, заданная вариантом
const int N = 3200 / 50;

// Функция сортировки массива
LPTHREAD_START_ROUTINE sort(int* mas) {
	int swap;
	for (int i = 0; i < N - 1; i++) {
		for (int j = 0; j < N - i - 1; j++) {
			if (mas[j] > mas [j + 1]) {
				swap = mas[j + 1];
				mas[j + 1] = mas[j];
				mas[j] = swap;
			}
		}
	}
	cout << "Array was sorted" << endl;
	return 0;
}

// Функция вывода массива на экран
LPTHREAD_START_ROUTINE mass_print(int* mas) {
	for (int i = 0; i < N - 1; i++)
		cout << mas[i] << " ";
	cout << endl;
	return 0;
}

int main() {
	int arr[N];
	
	// Заполнение массива случайными значениями
	for (int i = 0; i < N; i++)
		arr[i] = rand() % 10000;
	
	DWORD id1, id2;	// идентификаторы потоков
    HANDLE th1, th2;
    
    // Создание приостановленных потоков процедур sort и mass_print 
    th1 = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)sort, (LPVOID)arr, CREATE_SUSPENDED, &id1);
	th2 = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)mass_print, (LPVOID)arr, CREATE_SUSPENDED, &id2);
	
	// Задание приоритетов потоков
    SetThreadPriority(th1, THREAD_PRIORITY_NORMAL);			// сортировка
	SetThreadPriority(th2, THREAD_PRIORITY_NORMAL);	// вывод       
			                                                  
	// Активирование потоков 
	ResumeThread(th1);
	ResumeThread(th2);

	// Ожидание окончания потоков
    WaitForSingleObject(th1, INFINITE);
    WaitForSingleObject(th2, INFINITE);

	system("pause");
	return 0;
}