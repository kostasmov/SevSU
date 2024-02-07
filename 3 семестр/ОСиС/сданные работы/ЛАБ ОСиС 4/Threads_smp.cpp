#include <windows.h>
#include <iostream>
using namespace std;

// Значения, заданные по варианту
const int Nbuf = 9;	// длина буфера
const int N = 170;	// длина последовательности

// Буфер и его макс. заполненность
int arr[Nbuf];
int c = 0;	// текущая заполненность буфера
int m = 0;	// макс. заполненность буфера

// Дескрипторы семафоров
HANDLE f = CreateSemaphore(NULL, Nbuf, Nbuf, "SemaphoreFree");
HANDLE nonf = CreateSemaphore(NULL, 0, Nbuf, "SemaphoreNonFree");
HANDLE bin = CreateSemaphore(NULL, 1, 1, "SemaphoreBin");

// Поток ввода в буфер
LPTHREAD_START_ROUTINE input()
{
    int n = 510;
    for (int i = 0; i < N; i++)
    {
        WaitForSingleObject(f, INFINITE);
        WaitForSingleObject(bin, INFINITE);

        n -= 3;
        arr[i % Nbuf] = n;
        c++;
        if (c > m) m = c;

        ReleaseSemaphore(bin, 1, NULL);
        ReleaseSemaphore(nonf, 1, NULL);
    }
    return 0;
}

// Поток вывода из буфера
LPTHREAD_START_ROUTINE output()
{
    for (int i = 0; i < N; i++)
    {
        WaitForSingleObject(nonf, INFINITE);
        WaitForSingleObject(bin, INFINITE);

        cout << arr[i % Nbuf] << " ";
        if (((i + 1) % 17 == 0) && (i)) cout << endl;
        c--;

        ReleaseSemaphore(bin, 1, NULL);
        ReleaseSemaphore(f, 1, NULL);
    }
    return 0;
}

// Главная функция
int main()
{
    DWORD id[2];	// идентификаторы
    HANDLE th[2];	// дескрипторы

    // Создание потоков
    th[0] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)input, (LPVOID)(0), THREAD_PRIORITY_NORMAL, &id[0]);
    th[1] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)output, (LPVOID)(0), THREAD_PRIORITY_NORMAL, &id[1]);
    WaitForMultipleObjects(2, th, TRUE, INFINITE);

	// Максимальная заполненность (длина) буфера
	cout << endl << "Max buffer full - " << m;

    // Закрыть дескрипторы семафоров
    CloseHandle(f);
    CloseHandle(nonf);
    CloseHandle(bin);
}