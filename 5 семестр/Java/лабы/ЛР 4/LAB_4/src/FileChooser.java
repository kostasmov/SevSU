import java.io.File;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

// Класс для окна выбора файла для ввода-вывода файла
public class FileChooser
{
	private final JFileChooser chooser;	// компонент выбора файла

	public FileChooser()
	{
		chooser = new JFileChooser();
		chooser.setFileFilter(new FileNameExtensionFilter("Файл CSV", "csv"));
	}

	// Выбрать файл, из которого будут загружены данные
	public File getReadFile()
	{
		chooser.setDialogTitle("Открыть файл");
		int result = chooser.showOpenDialog(null);
		if (result == JFileChooser.APPROVE_OPTION)
		{
			return chooser.getSelectedFile();
	    }
		else
	    { return null; }
	}

	// Выбрать файл для сохранения данных
	public File getSaveFile()
	{
		chooser.setDialogTitle("Сохранить");
		int result = chooser.showSaveDialog(null);
		if (result == JFileChooser.APPROVE_OPTION)
		{
			return chooser.getSelectedFile();
	    }
		else
	    { return null; }
	}
}
