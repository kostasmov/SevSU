#include <iostream>
#include <windows.h>
#include <cstdlib>
#include <ctime>
using namespace std;

const int N = 75; 		// длинна массива
CRITICAL_SECTION crit; // критическая секция

// Заполнение массива
void setArray(int arr[N])
{
	srand( time(NULL) );
	for (int i = 0; i < N; i++)
		arr[i] = rand() % 101;
}

// Сортировка массива
void sortArray(int arr[N])
{
    int swap;
	for (int i = 0; i < N-1; i++)
	{
		int max = i;
		for (int j = i+1; j < N; j++)
			if (arr[j] > arr[max]) max = j;
		swap = arr[i];
		arr[i] = arr[max];
		arr[max] = swap;
	}
}

// Вывод массива
void showArray(int arr[N], int N_THR)
{
    for (int i = 0; i < N; i++)
        cout << N_THR << ": " << arr[i] << endl;
}

// Функция потока (ввод, сортировка, вывод)
LPTHREAD_START_ROUTINE Sort (int N_THR)
{
    int arr[N];
    setArray(arr);	// ввод
    sortArray(arr);	// сортировка

	// Обращение к критической секции
    EnterCriticalSection(&crit);

	cout << "Thread " << N_THR << endl;
    showArray(arr, N_THR);	// вывод

	// Освобождение критической секции
    LeaveCriticalSection(&crit);

    return 0;
}

// Главная функция
int main ()
{
    DWORD id[5];	// идентификаторы
    HANDLE th[5];	// дескрипторы

	// Инициализация критической секции
    InitializeCriticalSection(&crit);

	// Цикл запусков потоков Sort
    for (int i = 0; i < 5; i++)
        th[i] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)Sort, (LPVOID)(i+1), 0, &id[i]);

	// Ожидание окончания потоков и удаление критической секции
	WaitForMultipleObjects(5, th, TRUE, INFINITE);
    DeleteCriticalSection(&crit);
    
    return 0;
}