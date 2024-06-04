using System;

public class PlagiarismChecker
{
    public void CompareTexts(string text1, string text2)
    {
        int[,] matrix = new int[text1.Length + 1, text2.Length + 1];

        for (int i = 0; i <= text1.Length; i++)
        {
            matrix[i, 0] = i;
        }

        for (int j = 0; j <= text2.Length; j++)
        {
            matrix[0, j] = j;
        }

        for (int i = 1; i <= text1.Length; i++)
        {
            for (int j = 1; j <= text2.Length; j++)
            {
                if (text1[i - 1] == text2[j - 1])
                {
                    matrix[i, j] = matrix[i - 1, j - 1];
                }
                else
                {
                    matrix[i, j] = Math.Min(Math.Min(matrix[i - 1, j] + 1, matrix[i, j - 1] + 1), matrix[i - 1, j - 1] + 1);
                }
            }
        }

        int matchesCount = text1.Length + text2.Length - matrix[text1.Length, text2.Length];
        double percentage = (double)matchesCount / (double)(text1.Length + text2.Length) * 100;

        Console.WriteLine("Результат сравнения текстов:");
        Console.WriteLine($"Общее число совпадений: {matchesCount}");
        Console.WriteLine($"Процентное соотношение совпадений: {percentage}%");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        string t1 = "Я не знаю, как мне быть";
        string t2 = "Я не знаю, что мне делать";

        PlagiarismChecker checker = new PlagiarismChecker();
        checker.CompareTexts(t1, t2);
    }
}
