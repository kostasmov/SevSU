#include "mpi.h"
#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>

using namespace std;

void master();
void slave();
void printMatrix(int* matrix, int rows, int cols, string name);

const int N = 3;    // Число строк матрицы 1
const int M = 4;    // Число столбцов матрицы 1 | строк матрицы 2 
const int K = 4;    // Число столбцов матрицы 2


/*  Вариант 1 - Перемножение матриц
    Программа умножает две матрицы. Размеры матриц – N*M и M*K. 
    Каждый процесс определяет произведение одной строки матрицы 1 на все столбцы матрицы 2. 
    Результаты возвращаются в родительскую задачу. */

int main(int argc, char* argv[])
{
    int rank;

    MPI_Init(&argc, &argv);                 // Запуск MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);   // Запись номера процесса в rank

    rank ? slave() : master();              // нулевой процесс главный, остальные подчинённые

    MPI_Finalize();
    return 0;
}


// ====== Главный процесс (планировщик заданий) ======
void master()
{
    int proc_count;                               // количество процессов
    MPI_Comm_size(MPI_COMM_WORLD, &proc_count);

    if (proc_count <= N)
    {
        cout << "Can't complete work: not anough slave processes" << endl;
        return;
    }

    // матрицы (множители)
    int matrix1[N][M] = {};
    int matrix2[M][K] = {};

    // итоговая матрица-произведение
    int result_matrix[N][K] = {};

    // ---------- Чтение матриц из файла ----------
    ifstream file("C:/matrix.txt");

    if (!file) {
        cout << "There is no input file" << endl;
        return;
    }
    
    // чтение матрицы 1
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            file >> matrix1[i][j];
        }
    }

    // чтение матрицы 2
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < K; j++)
        {
            file >> matrix2[i][j];
        }
    }

    file.close();
    // --------------------------------------------

    printMatrix(&matrix1[0][0], N, M, "Matrix 1");
    printMatrix(&matrix2[0][0], M, K, "Matrix 2");

    MPI_Request send_request[N * 2] = {};   // дескрипторы отправок

    // отправление исполнителям строк и матрицы
    for (int i = 0; i < N; i++)
    {
        MPI_Isend(matrix1[i], M, MPI_INT, i + 1, 1, MPI_COMM_WORLD, &send_request[i]);
        MPI_Isend(matrix2, M * K, MPI_INT, i + 1, 2, MPI_COMM_WORLD, &send_request[N * 2 - i - 1]);
    }

    MPI_Waitall(N * 2, send_request, MPI_STATUSES_IGNORE);

    MPI_Request recv_request[N] = {};   // дескрипторы возвратов

    // получение результатов
    for (int i = 0; i < N; i++)
    {
        MPI_Irecv(result_matrix[i], K, MPI_INT, i + 1, 3, MPI_COMM_WORLD, &recv_request[i]);
    }

    MPI_Waitall(N, recv_request, MPI_STATUSES_IGNORE);

    // вывод результата
    printMatrix(&result_matrix[0][0], N, K, "Result matrix");
}


// ======= Подчинённые процессы (вычислительные задачи) =======
void slave()
{
    MPI_Request get_request[3];

    int row[M];         // буфер умножаемой строки
    int matrix[M][K];   // матрица-множитель

    int result[K] = {}; // строка-произведение
    
    // приём строки и матрицы для перемножения
    MPI_Irecv(row, M, MPI_INT, 0, 1, MPI_COMM_WORLD, &get_request[0]);
    MPI_Irecv(matrix, M * K, MPI_INT, 0, 2, MPI_COMM_WORLD, &get_request[1]);

    MPI_Waitall(2, get_request, MPI_STATUSES_IGNORE);
    
    // произведение строки на матрицу
    for (int j = 0; j < K; j++)
    {
        result[j] = 0;
        for (int i = 0; i < M; i++) 
        {
            result[j] += row[i] * matrix[i][j];
        }
    }

    // отправка результата в master
    MPI_Isend(result, K, MPI_INT, 0, 3, MPI_COMM_WORLD, &get_request[2]);
}


// Вывод матрицы
static void printMatrix(int* matrix, int rows, int cols, string name = "")
{
    if (!name.empty()) 
        cout << name << ":\n";

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            cout << setw(2) << matrix[i * cols + j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}