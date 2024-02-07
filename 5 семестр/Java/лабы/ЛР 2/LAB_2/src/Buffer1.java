import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Buffer1 extends Buffer
	implements IBufferComputable, IBufferPrintable, IBufferSortable, IBufferStorable
{
	public Buffer1(int size)	// конструктор класса
	{
		super(size);
	}
	
	@Override
	public void PrintInfo()	// вывод информации о буфере
	{
		System.out.printf("ID: %d. Тип: double. Размер: %d\n", bufID, bufSize);
	}

	@Override
	public void Print()	// вывод содержимого буфера
	{
		System.out.print("Содержимое буфера: ");
		for (int i = 0; i < bufSize; i++)
		{
			System.out.printf("%.3f ", bufArray[i]);
		}
		System.out.printf("\n");
	}

	@Override
	public void PrintFirstN(int n)	// первые N элементов
	{
		System.out.printf("Первые %d элементов: ", n);
		for (int i = 0; i < n; i++)
		{
			System.out.printf("%.3f ", bufArray[i]);
		}
		System.out.printf("\n");
	}

	@Override
	public void PrintLastN(int n)	// последние N элементов
	{
		System.out.printf("Последние %d элементов: ", n);
		for (int i = bufSize-10; i < bufSize; i++)
		{
			System.out.printf("%.3f ", bufArray[i]);
		}
		System.out.printf("\n");
	}

	@Override
	public void Sort()	// сортировка буфера (Шелла)
	{
		int i, j;
		for (int gap = bufSize / 2; gap > 0; gap /= 2)
		{
			for (i = gap; i < bufSize; i++)
			{
				double temp = bufArray[i];
				for (j = i; j >= gap && bufArray[j - gap] > temp; j -= gap)
				{
					bufArray[j] = bufArray[j - gap];
				}
				bufArray[j] = temp;
			}
		}
		System.out.println("Сортировка выполнена");
	}
	
	@Override
	public void Max()	// максимальный элемент
	{
		double max = bufArray[0];
		for (int i = 1; i < bufSize; i++)
		{
			if (bufArray[i] > max)
			{
				max = bufArray[i];
			}
		}
		System.out.printf("Максимальное значение: %.3f\n", max);
	}

	@Override
	public void Min()	// минимальный элемент
	{
		double min = bufArray[0];
		for (int i = 1; i < bufSize; i++)
		{
			if (bufArray[i] < min)
			{
				min = bufArray[i];
			}
		}
		System.out.printf("Минимальное значение: %.3f\n", min);
	}

	@Override
	public void Sum()	// сумма элементов буфера
	{
		double sum = 0.0;
		for (int i = 1; i < bufSize; i++)
		{
			sum += bufArray[i];
		}
		System.out.printf("Сумма элементов: %.3f\n", sum);
	}

	@Override	// вывод в файл одной строкой
	public void SaveOneLine(String filename) throws IOException
	{
		try
		{
			PrintWriter writer = new PrintWriter(new FileWriter(filename));
			//writer.println("");
			for (int i = 0; i < bufSize; i++)
			{
				writer.printf("%.3f ", bufArray[i]);
			}
			writer.close();
		} catch (IOException e) {
			throw e;
		}
	}

	@Override	// вывод в файл построчно
	public void SaveSeparateLines(String filename) throws IOException
	{
		try
		{
			PrintWriter writer = new PrintWriter(new FileWriter(filename));
			for (int i = 0; i < bufSize; i++)
			{
				writer.printf("%.3f\n", bufArray[i]);
			}
			writer.close();
		} catch (IOException e) {
			throw e;
		}
	}
}
