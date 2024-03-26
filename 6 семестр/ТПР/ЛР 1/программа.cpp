#include <iostream>
using namespace std;

const int n = 7;	// число решений

// вывод матрицы отношений
void printA(int a[n][n]) 
{
	for (int i = 0; i < n; i++) 
	{
		for (int j = 0; j < n; j++)
			cout << a[i][j] << " ";
		cout << endl;
	}
	cout << endl;
}

int main()
{
	int a[n][n] = {
		{0, 1, 1, 0, 0, 0, 0},
		{0, 0, 1, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 1, 1},
		{0, 1, 0, 0, 0, 1, 0},
		{0, 1, 0, 1, 0, 1, 0},
		{0, 0, 0, 0, 0, 0, 1},
		{0, 0, 0, 0, 0, 0, 0}
	};
	
	/*int a[n][n] = {
		{0, 1, 1, 0, 1},
		{0, 0, 1, 1, 0},
		{0, 0, 0, 1, 1},
		{0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0}
	};*/
	
	printA(a);
	
	int MaxR[n];		// массив упорядоченных решений
	int K = 0, K1 = 0;	// количество элементов, добавленных в MaxR
	int count = n;		// счётчик
	int layer = 1;		// текущий ярус

	while (count > 0) 
	{
		cout << "Layer " << layer++ << ": ";
		int done = 0;
		
		// определение исключаемых элементов
		for (int i = 0; i < n; i++) 
		{
			int sum = 0;
			for (int j = 0; j < n; j++) 
				sum += a[i][j];	
			if (sum == 0) 
			{
				cout << "x" << i + 1 << " ";
				MaxR[K++] = i;
				done++;
			}
		}
		cout << endl;
		
		if (!done) 
		{
			cout << "\nError: graph contains contours";
			return 0;
		}
		
		// обнуление отношений с исключаемыми элементами
		for (int q = K1; q < K; q++) 
		{
			for (int x = 0; x < n; x++)
			{
				a[x][MaxR[q]] = 0;	
			}
		}

		// исключение элементов, добавленных в MaxR
		for (int q = K1; q < K; q++)
		{
			for (int x = 0; x < n; x++)
			{
				a[MaxR[q]][x] = 1;	
			}
		}
			
		printA(a);
		
		K1 = K; 
		count = n - K;
	}
	
	// вывод упорядоченных результатов
	cout << "Multiple solutions: ";
	for (int i = 0; i < n; i++)
		cout << "x" << MaxR[i] + 1 << " ";
}