import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collections;
import java.util.LinkedList;

public class Task3
{
	private LinkedList<CD> data;
	
	// Конструктор класса (считывает данные из файла)
	public Task3(File input) throws IOException
	{
		data = new LinkedList<CD>();
		
		try (BufferedReader reader = new BufferedReader(new FileReader(input)))
		{
			String line;
            while ((line = reader.readLine()) != null)
            {
            	String[] params = line.split(";");
                CD cd = new CD(params[0], params[1], Integer.parseInt(params[2]), Integer.parseInt(params[3]));
                data.add(cd);
            }
            reader.close();
		}
		catch (NumberFormatException | ArrayIndexOutOfBoundsException e)	
		{
			throw new IllegalArgumentException("Ошибка считывания файла ввода");
		}
	}

	public void printAll()	// вывод элементов
	{
		int i = 0;
		for (CD element : data)
		{
			System.out.printf("%d) %s\n", ++i, element.toString());
		}
	}
	
	public void execute(File file) throws IOException
	{
		System.out.println("--- Выполнение работы с LinkedList ---");

		System.out.println("Вывод содержимого (до сортировки):");
		printAll();

		System.out.println("\nВывод содержимого (после сортировки):");
		//Collections.sort(data, Collections.reverseOrder());	// сортировка через Comparable
		Collections.sort(data, new MyComp());					// сортировка через Comparator
		printAll();

		saveToFile(file);
		System.out.println("\nКоллекция записана в файл " + file);
		
		System.out.println("--- Окончание работы с LinkedList ---\n");
	}

	// Запись данных из контейнера в файл (текстовый)
	public void saveToFile(File file) throws IOException
	{
		BufferedWriter writer = new BufferedWriter(new FileWriter(file));
        for (CD element : data)
        {
            writer.write(element.toString());
            writer.newLine();
        }
        writer.close();
	}
}
