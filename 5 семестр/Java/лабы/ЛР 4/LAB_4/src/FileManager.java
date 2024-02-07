import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;

// Класс для работы с файловым вводом-выводом
public class FileManager
{
	private File file = null;	// выбранный файл

	public FileManager(File file)	// конструктор
	{
		this.file = file;
	}

	// Считывание данных из файла
	public HashSet<Auto> readSet() throws IOException
	{
		try (BufferedReader reader = new BufferedReader(new FileReader(file)))
		{
			HashSet<Auto> data = new HashSet<Auto>();
			String line;
            while ((line = reader.readLine()) != null)
            {
            	String[] params = line.split(";");
            	params[2] = params[2].replace(",", ".");
                Auto car = new Auto(params[0], Integer.parseInt(params[1]), Float.parseFloat(params[2]), 
                		Integer.parseInt(params[3]));
                data.add(car);
            }
            reader.close();
            return data;
            
		}
		catch (NumberFormatException | ArrayIndexOutOfBoundsException e)	
		{
			throw new IllegalArgumentException("Ошибка считывания файла ввода");
		}
	}

	// Запись данных в файл
	public void writeSet(Iterator<Auto> collection) throws IOException
	{
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(file)))
		{
	        while (collection.hasNext())
	        {
	            Auto auto = collection.next();
	            writer.write(auto.toString() + '\n');
	        }
	    }
	}
}