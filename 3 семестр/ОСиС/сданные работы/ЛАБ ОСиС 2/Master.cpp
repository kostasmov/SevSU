#include <windows.h>
#include <iostream>
#include <string.h>
#include <cstdio>
using namespace std;

// Приоритеты процессов, заданные вариантом
const int prts[3][3] = { {3, 2}, {3, 3}, {3, 1} };

int main() {
	SYSTEMTIME time;
	
	// Название вызываемой команды записываем в массив
	char cmd[10] = "Sort.exe";

	// Данные запускаемого процесса
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	memset(&si, 0, sizeof(si));
	si.cb = sizeof(si);
	
	// Массив с названиями классов приоритетов
	char prtClass[3][30];
	strcpy(prtClass[0], "IDLE_PRIORITY_CLASS");
	strcpy(prtClass[1], "NORMAL_PRIORITY_CLASS");
	strcpy(prtClass[2], "HIGH_PRIORITY_CLASS");
	
	// Цикл запуска процессов Sort.exe
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j <= 1; j++) {
			
			// Заполнение заголовка процесса
			char t[200] = "Process: ";
			sprintf(t + strlen(t), "%d.%d; Priority: %s", i+1, j+1, prtClass[prts[i][j]-1]);
			si.lpTitle = t;
			
			// Вызов процесса с определённым классом приоритета
			switch (prts[i][j]) {
				case 1: CreateProcess(NULL, cmd, NULL, NULL, FALSE, CREATE_NEW_CONSOLE | IDLE_PRIORITY_CLASS, NULL, NULL, &si, &pi); break;
				case 2: CreateProcess(NULL, cmd, NULL, NULL, FALSE, CREATE_NEW_CONSOLE | NORMAL_PRIORITY_CLASS, NULL, NULL, &si, &pi); break;
				case 3: CreateProcess(NULL, cmd, NULL, NULL, FALSE, CREATE_NEW_CONSOLE | HIGH_PRIORITY_CLASS, NULL, NULL, &si, &pi); break;
			}	
		}
		
		// Ожидание окончания процессов и вывод текущего времени
		WaitForSingleObject(pi.hProcess, INFINITE);
		GetSystemTime(&time);
		cout << "End of processes " << i << ": ";
		cout << time.wMinute << "." << time.wSecond << "." << time.wMilliseconds << endl;
	}
}