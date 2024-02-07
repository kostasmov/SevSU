#include <windows.h>
#include <iostream>
#include <cstring>
using namespace std;

int main(int argc, char *argv[])
{
	// Информация о запуске нового процесса
	STARTUPINFO si;
	memset(&si, 0, sizeof(si));
	si.cb = sizeof(si);
	
	// Идентификатор и дескриптор нового процесса
	PROCESS_INFORMATION pi;
	
	// Запуск процессов
	for (int N_PRC = 1; N_PRC <= 5; N_PRC++)
	{
		char cmd[300] = "Sort3.exe";
		sprintf(cmd + strlen(cmd), " %d", N_PRC);
		if (!CreateProcess(NULL, cmd, NULL, NULL, FALSE, NORMAL_PRIORITY_CLASS, NULL, NULL, &si, &pi))
			cout << "Master3: Error, can't call Sort3.exe" << endl;
	}                       
	
	// Закрытие процессов
	WaitForSingleObject(pi.hProcess, INFINITE);                          
}