#include <windows.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

const int N = 75;

int main(int argc, char *argv[])
{	
	// Проверка наличия параметра N_PRC
	if (argc != 2)
	{
		cout << "Sort3: Program must be called by Master3.exe" << endl;
		return 0;
	}
	
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
	
	// Вывод массива
	cout << "Sort3: Process "<< N_PRC << endl;
	for (int i = 0; i < N; i++)
		cout << N_PRC << ": " << arr[i] << endl;
	
	return 1;
}