#include <windows.h>
#include <iostream>
#include <cstring>
using namespace std;

int main(int argc, char *argv[])
{
	HANDLE mtx = CreateMutex(NULL, FALSE, "MyMutex");	// мьютекс
	
	// Информация о запуске нового процесса
	STARTUPINFO si;
	memset(&si, 0, sizeof(si));
	si.cb = sizeof(si);
	
	// Идентификатор и дескриптор нового процесса
	PROCESS_INFORMATION pi;
	
	// Запуск процессов
	for (int N_PRC = 1; N_PRC <= 5; N_PRC++)
	{
		char cmd[300] = "Sort3_mtx.exe";
		sprintf(cmd + strlen(cmd), " %d", N_PRC);
		if (!CreateProcess(NULL, cmd, NULL, NULL, FALSE, NORMAL_PRIORITY_CLASS, NULL, NULL, &si, &pi))
			cout << "Master3_mtx: Error, can't call Sort3_mtx.exe" << endl;
		//WaitForSingleObject(pi.hProcess, INFINITE);
	} 
	
	// Ожидание конца процессов и закрытие мьютекса
	WaitForSingleObject(pi.hProcess, INFINITE);
	CloseHandle(mtx);                                             
}