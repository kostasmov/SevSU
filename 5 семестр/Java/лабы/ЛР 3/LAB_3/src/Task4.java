import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Task4
{
	private HashMap<String, CD> data;

	// Конструктор класса (считывает данные из файла)
	public Task4(File input) throws IOException
	{
		data = new HashMap<String, CD>();
		
		try (BufferedReader reader = new BufferedReader(new FileReader(input)))
		{
			String line;
            while ((line = reader.readLine()) != null)
            {
            	String[] params = line.split(";");
            	String key = params[0];
                CD value = new CD(params[0], params[1], Integer.parseInt(params[2]), Integer.parseInt(params[3]));
                data.put(key, value);
            }
            reader.close();
		}
		catch (NumberFormatException | ArrayIndexOutOfBoundsException e)	
		{
			throw new IllegalArgumentException("Ошибка считывания файла ввода");
		}
	}
	
	private void printAll()	// вывод содержимого коллекции
	{
		for (Map.Entry<String, CD> entry : data.entrySet())
		{
            String key = entry.getKey();
            CD value = entry.getValue();
            System.out.println(key + ": " + value.toString());
        }
	}

	public void execute()
	{
		System.out.println("--- Выполнение работы с HashMap ---");

		System.out.println("Вывод содержимого:");
		printAll();

		System.out.print("Введите имя альбома для поиска: ");
		CD founded = data.get(readKey());
		if (founded != null)
		{
			System.out.println("Найдено: " + founded.toString());
		}
		else 
		{
			System.out.println("Ошибка: указанный элемент не найден");
		}

		System.out.println("--- Окончание работы с HashMap ---");
	}

	private String readKey()	// ввод строчного параметра
	{
		Scanner scanner = new Scanner(System.in);
		String key = scanner.next();
		return key;
	}
}
