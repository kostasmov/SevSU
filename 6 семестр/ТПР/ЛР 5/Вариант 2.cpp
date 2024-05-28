﻿#include <stdio.h>
#include <stdlib.h>
#include <search.h>
#include <iostream>
#include <iomanip>

using namespace std;

int comp(const void* a, const void* b) {
    return (*(int*)b - *(int*)a);
}

bool search0(int N_Model[], int n_krit) {
    int i;
    for(i = 0; i < n_krit; i++) {
        if(N_Model[i] == 0) {
            return 1;
        }
    }
    return 0;
}

int main()
{
    setlocale(LC_ALL, "Russian");

    const int n_krit = 5, n_x = 8;

	// Матрица векторнх оценок
    int Shcal_oc[n_x][n_krit] = {
      { 3, 5, 5, 4, 4 },
      { 4, 4, 4, 5, 4 },
      { 5, 4, 3, 3, 5 },
      { 3, 5, 3, 5, 3 },
      { 4, 2, 4, 5, 5 },
      { 3, 5, 3, 5, 3 },
      { 5, 3, 4, 3, 4 },
      { 4, 5, 3, 4, 3 }
    };

    int ne_sravnim_resh[n_x] = { 0 };
    int inf_vazhnosti[n_krit] = { 4, 1, 6, 2, 1 };
    int inf_vazhnosti_kop[n_krit] = { 4, 1, 6, 2, 1 };
    const int  kol_el_vekt_oc = 14;
    int matr_vekt_oc[n_x][kol_el_vekt_oc] = { 0 };
    int matr_predpocht[n_x][n_x] = { 0 };
    int domin_prizn[n_krit] = { 0 };
    int counter = 0;
    int j = 0;

	// Вывод векторных оценок
    cout << "      K1 K2 K3 K4 K5" << endl;
    for (int i = 0; i < n_x; i++) {
        cout << " x" << i + 1 << " = ( ";
        for (int q = 0; q < n_krit; q++)
            cout << Shcal_oc[i][q] << " ";
        cout << ");" << endl;
    }

    // Матрица степеней важности
    int importance_matrix[n_krit][n_krit] = {
      { 0, 0, 0, 2, 0 },
      { 0, 0, 0, 0, 1 },
      { 0, 0, 0, 3, 0 },
      { 0, 2, 0, 0, 0 },
      { 0, 1, 0, 0, 0 }
    };

    // Вывод матрицы степеней важности
    cout << "\nМатрица степеней важности:\n";
    for (int i = 0; i < n_krit; i++)
    {
        for (int j = 0; j < n_krit; j++)
		{
            cout << setw(2) << importance_matrix[i][j];
        }
        cout << endl;
    }

    cout << endl;

    // Расчёт N-модели
    int N_Model[n_krit] = { 0, 0, 0, 0, 0 };
    int temp;

    for (int i = 0; i < 5; i++) {
        int count = 0;
        for (int j = 0; j < 5; j++) {
            count += importance_matrix[i][j];
        }
        if (count <= 1) {
            N_Model[i] = 1;
            temp = i;
        }
    }

	while (search0(N_Model, n_krit)) {
		int temp2 = -1;
        for (int j = 0; j < 5; j++) {
            if (importance_matrix[j][temp] != 0) {
                N_Model[j] = N_Model[temp] * importance_matrix[j][temp];
                
                if (importance_matrix[j][temp] != 1 || temp2 == -1) {
                    temp2 = j;
                }
            }
        }
        temp = temp2;
    }
    
    cout << "Формирование N-модели: N = { ";
    for (int i = 0; i < n_krit; i++) {
      if (i)
        cout << ", ";
      cout << N_Model[i];
    }
    cout << " };";

    for (int i = 0; i < n_x; i++) {
        for (int k = 0; k < n_x; k++) {
            if (k != i) {
                for (j = 0; j < n_krit; j++) {
                    if (Shcal_oc[i][j] >= Shcal_oc[k][j]) {
                        domin_prizn[j] = 1;
                    }
                }
                for (int q = 0; q < n_krit; q++) {
                    if (domin_prizn[q] == 1)
                        counter++;
                }
                if (counter == n_krit) {
                    matr_predpocht[i][j] = 1;
                }
                else if (!counter) {
                    matr_predpocht[j][i] = 1;
                }
                else {
                    matr_predpocht[i][j] = 1;
                    matr_predpocht[j][i] = 1;
                }

                for (int t = 0; t < n_krit; t++) {
                    domin_prizn[t] = 0;
                    counter = 0;
                }
            }
        }
    }

    int vect_oc[n_x][kol_el_vekt_oc] = { { 0 },{ 0 },{ 0 },{ 0 },{ 0 },{ 0 },{ 0 },{ 0 } };
    for (int i = 0; i < n_x; i++) {
        int k = 0;
        for (int i = 0; i < n_krit; i++)
            inf_vazhnosti_kop[i] = inf_vazhnosti[i];
        for (j = 0; j < kol_el_vekt_oc; j++) {
            if (inf_vazhnosti_kop[k] > 0)
            {
                vect_oc[i][j] = Shcal_oc[i][k];
                inf_vazhnosti_kop[k]--;

            }
            else
            {
                k++;
                j--;
            }
        }
    }

    for (int i = 0; i < n_x; i++) {
        qsort(vect_oc[i], kol_el_vekt_oc, sizeof(int), comp);
    }

    cout << endl;

    cout << endl << "Модифицированные векторные оценки" << endl;
    for (int i = 0; i < n_x; i++) {
        cout << " X" << (i + 1) << " = { ";
        for (j = 0; j < kol_el_vekt_oc; j++) {
            cout << vect_oc[i][j] << " ";
        }
        cout << "};" << endl;
    }

    for (int i = 0; i < n_x; i++) {
        for (int k = 0; k < n_x; k++) {
            if (k != i) {
                counter = 0;
                for (j = 0; j < kol_el_vekt_oc; j++) {
                    if (ne_sravnim_resh[i] == 1)
                        break;
                    if (vect_oc[i][j] >= vect_oc[k][j]) {
                        domin_prizn[j] = 1;
                    }
                }
                for (int q = 0; q < kol_el_vekt_oc; q++) {
                    if (domin_prizn[q] == 1)
                        counter++;
                }
                if (counter == kol_el_vekt_oc) {
                    ne_sravnim_resh[k] = 1;
                }


                for (int t = 0; t < n_krit; t++) {
                    domin_prizn[t] = 0;
                    counter = 0;
                }
            }
        }
    }

    cout << endl;

    cout << "Несравнимые решения: ";
    for (int i = 0; i < n_x; i++) {
        if (ne_sravnim_resh[i] == 0) {
            cout << "X(" << i + 1 << ") ";
        }
    }
    
    cout << endl;
    system("pause");
}