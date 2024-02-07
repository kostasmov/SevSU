import java.io.File;
import java.io.IOException;

public class Lab3Java
{
	private static File input = null;
	private static File output = null;
	
	public static void main (String[] args)
	{
		try
		{
			readArguments(args);
			new Task2(input).execute();
			new Task3(input).execute(output);
			new Task4(input).execute();
		}
		catch (IllegalArgumentException e)
		{
			System.err.println(e.getMessage());
		}
		catch (IOException e)
		{
			System.err.println("Ошибка ввода-вывода");
		}
	}
	
	// Обработка аргументов командной строки
	public static void readArguments(String[] args)	
	{
		try
		{
			for (int i = 0; i < args.length; ++i)
			{
				switch (args[i])
				{
				case "-i":		// параметр файла ввода
					input = new File(args[++i]);
					break;
				case "-o":		// параметр файла вывода
					output = new File(args[++i]);
					break;
				default:		// ошибка параметра
					throw new IllegalArgumentException("Ошибка: параметр " + args[0] + " не распознан");
				}
			}
		}
		catch (IndexOutOfBoundsException e)
		{
			throw new IllegalArgumentException("Ошибка: нет значения после параметра");
		}
		finally
		{
			if (input == null)
				throw new IllegalArgumentException("Ошибка: не введён файл ввода");
			if (output == null)
				throw new IllegalArgumentException("Ошибка: не введён файл вывода");
		}
	}
}
