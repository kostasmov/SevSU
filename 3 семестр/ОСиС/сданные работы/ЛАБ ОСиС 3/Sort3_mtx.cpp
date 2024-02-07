#include <windows.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

const int N = 75;	// длина массива

int main(int argc, char *argv[])
{	
	// Проверка наличия параметра N_PRC
	if (argc != 2)
	{
		cout << "Sort3_mtx: Program must be called by Master3_mtx.exe" << endl;
		return 0;
	}
	
	// Открытие объекта мьютекса (или ошибка)
	HANDLE mtx = OpenMutex(SYNCHRONIZE, FALSE, "MyMutex");
	if (!mtx) return 0;
	
	// N_PRC - номер процесса, переданный через Master.exe
	int N_PRC = atoi(argv[1]);
	
	// Заполнение массива
	int arr[N];
	srand( time(NULL) );
	for (int i = 0; i < N; i++)
		arr[i] = rand() % 101;
	
	// Сортировка (прямой выбор)
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
	
	// Захват объекта мьютекса
	WaitForSingleObject(mtx, INFINITE);
	
	// Вывод массива
	cout << "Sort3_mtx: Process "<< N_PRC << endl;
	for (int i = 0; i < N; i++)
		cout << N_PRC << ": " << arr[i] << endl;
	
	// Освобождение мьютекса
	ReleaseMutex(mtx);

	return 1;
}