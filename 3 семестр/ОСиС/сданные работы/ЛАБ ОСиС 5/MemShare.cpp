#include <iostream>
#include <windows.h>
#include <climits>
using namespace std;

// Константы
const int N_PAGE = 3;						// кол-во страниц (задано вариантом)
const int PAGE_SIZE = 4096;					// размер страницы в байтах
const int TOTAL_SIZE = N_PAGE * PAGE_SIZE;	// память под все страницы

// Начальные данные о типе массива
typedef short arr_type;
const int MAX = SHRT_MAX;
const int ARR_LEN = TOTAL_SIZE / sizeof(arr_type);

// Главная функция - заполняет массив, вызывает процесс его сортировки и выводит на экран
int main()
{
    HANDLE mutex = CreateMutex(NULL, TRUE, "MyMytex");
    
    // запуск процесса MemSort (в режиме ожидания)
    STARTUPINFO si = { 0 };
    si.cb = sizeof(STARTUPINFO);
	PROCESS_INFORMATION pi = { 0 };
    CreateProcess(NULL, "MemSort.exe", 0, NULL, FALSE, 0, NULL, NULL, &si, &pi);

    // выделение памяти под массив и его заполнение
    LPVOID base_mem = VirtualAlloc(NULL, TOTAL_SIZE, MEM_COMMIT, PAGE_READWRITE);
    arr_type* arr = (arr_type*) base_mem;
    for (int i = 0; i < ARR_LEN; i++)
    {
    	arr[i] = rand() % MAX;
	}
    
	// перевод режима доступа (только для чтения)
	DWORD old_protec;
    VirtualProtect(base_mem, TOTAL_SIZE, PAGE_READONLY, &old_protec);
	
	// создание объекта отображения для памяти общего доступа
    HANDLE file_map = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, TOTAL_SIZE, "memshare");
    LPVOID pub = MapViewOfFile(file_map, FILE_MAP_ALL_ACCESS, 0, 0, TOTAL_SIZE);

	// перенос данных из массива 
    CopyMemory(pub, base_mem, TOTAL_SIZE);

	// запуск сортировки MemSort
    ReleaseMutex(mutex);
    WaitForSingleObject(pi.hProcess, INFINITE);
	
	// вернуть возможность записи в массив
    VirtualProtect(base_mem, TOTAL_SIZE, PAGE_READWRITE, &old_protec);
    CopyMemory(base_mem, pub, TOTAL_SIZE);

	// вывод массива
    for (int i = 0; i < ARR_LEN; i++)
    {
    	cout << arr[i] << " ";	
	}

	// освобождение памяти
    VirtualFree(base_mem, TOTAL_SIZE, MEM_RELEASE);
    UnmapViewOfFile(pub);
    CloseHandle(file_map);
    
	return 1;
}
