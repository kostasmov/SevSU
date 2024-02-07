import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Scanner;

public class Task2
{
	private HashSet<CD> data;
	
	// Конструктор класса (считывает данные из файла)
	public Task2(File input) throws IOException
	{
		data = new HashSet<CD>();
		
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
		for (CD element : data)
		{
			System.out.println(element);
		}
	}
	
	public void execute()	// выполнение операций с коллекцией
	{
		System.out.println("--- Выполнение работы с HashSet ----");
		
		System.out.println("Вывод содержимого:");
		printAll();
		
		System.out.print("Введите имя альбома для поиска: ");
		CD founded = findByAlbum(readKey());
		if (founded != null)
		{ System.out.println("Найдено: " + founded.toString()); }
		else 
		{ System.out.println("Ошибка: указанный элемент не найден"); }

		System.out.println("--- Окончание работы с HashSet ---\n");
	}
	
	public CD findByAlbum(String album)	// поиск по названию альбома
	{
		CD foundedElement = null;
		for (CD element : data)
		{
			if (element.albumTitle.equals(album))
			{
				foundedElement = element;
				break;
			}
		}
		return foundedElement;
	}

	private String readKey()	// ввод строчного параметра
	{
		Scanner scanner = new Scanner(System.in);
		String key = scanner.next();
		return key;
	}
}
