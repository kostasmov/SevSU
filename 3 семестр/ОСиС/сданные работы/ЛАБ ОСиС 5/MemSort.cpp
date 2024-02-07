#include <windows.h>
#include <climits>

// Константы
const int N_PAGE = 3;						// кол-во страниц (задано вариантом)
const int PAGE_SIZE = 4096;					// размер страницы в байтах
const int TOTAL_SIZE = N_PAGE * PAGE_SIZE;	// память под все страницы

// Начальные данные о типе массива
typedef short arr_type;
const int MAX = SHRT_MAX;
const int ARR_LEN = TOTAL_SIZE / sizeof(arr_type);

// Функция сортировки массива (метод вставки)
void sort(arr_type* arr, int len)
{
	for (int i = 1; i < len; i++)
	{
		int temp = arr[i];
		int j = i-1; 
		while ((j >= 0) && (arr[j] > temp))
		{
			arr[j + 1] = arr[j];
			arr[j] = temp;
			j--;
		}
	}
}

// Главная функция
int main()
{
	// ожидание освобождения мьютекса
    HANDLE mutex = OpenMutex(MUTEX_ALL_ACCESS, FALSE, "MyMutex");
    WaitForSingleObject(mutex, INFINITE);

	// открыть память общего доступа
    HANDLE shared = OpenFileMapping(FILE_MAP_ALL_ACCESS, FALSE, "memshare");
    arr_type* arr = (arr_type*) MapViewOfFile(shared, FILE_MAP_ALL_ACCESS, 0, 0, TOTAL_SIZE);

    sort(arr, ARR_LEN);
    
    // освобождение мьютекса и памяти
    ReleaseMutex(mutex);
    UnmapViewOfFile((LPVOID) arr);
    CloseHandle(shared);

    return 1;
}
