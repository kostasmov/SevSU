import java.io.FileInputStream;
import java.io.PrintStream;
import java.util.Scanner;
import java.util.InputMismatchException;
import java.io.IOException;
import java.io.FileNotFoundException;

public class Main {

	public static void main(String[] args)
	{
		int i = 0;
		try
		{
			for (; i < args.length; ++i)	// перебор параметров с консоли
			{
				switch (args[i])
				{
				case "-i":	// перенаправление ввода из файла
					i++;
					System.setIn(new FileInputStream(args[i]));
					break;
				case "-o":	// перенаправление вывода в файл
					i++;
					System.setOut(new PrintStream(args[i]));
					break;
				default:	// ошибка параметра
					throw new IllegalArgumentException();
				}
			}
			
			// Считывание переменных a, b, c
			Scanner scanner = new Scanner(System.in);
			int a = scanner.nextInt();
			int b = scanner.nextInt();
			int c = scanner.nextInt();
			scanner.close();
			
			// Дискриминант и корни квадратного уравнения
			double D = b * b - 4 * a * c;
			if (D < 0) { throw new ArithmeticException("Error: discriminant is less than zero"); }
			double x1 = (-b + Math.sqrt(D)) / (2*a);
			double x2 = (-b - Math.sqrt(D)) / (2*a);
			
			// Вывод результата
			if (x1 != x2) { System.out.println(String.format("Solutions: %.2f  %.2f", x1, x2));}
			else {System.out.println(String.format("Solution: %.2f", x1));}
			
		}
		catch (FileNotFoundException e)	// файл не найден
		{
			System.err.printf("Error: Can't find '%s' file", args[i]);
		}
		catch (IndexOutOfBoundsException e)	// недостающий параметр <filename>
		{
			System.err.printf("Error: Expected filename after %s param", args[i - 1]);
		} 
		catch (IllegalArgumentException e)	// неподдерживаемый параметр
		{
			System.err.printf("Error: Parametr %s is unknown", args[i]);
		}
		catch (InputMismatchException e)	// неверная запись числа
		{
			System.err.println("Error: Incorrect number format");
		}
		catch (ArithmeticException e)	// вычислительная ошибка
		{
			System.err.println(e.getMessage());
		}	
	}	
}
