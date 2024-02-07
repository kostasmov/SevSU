import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import javax.swing.table.AbstractTableModel;

// Модель табличного представления множества объектов класса Auto
public class AutoTableModel extends AbstractTableModel
{
	private static final long serialVersionUID = 6181788579049573897L;
	private final HashSet<Auto> data = new HashSet<Auto>();
	
	private final String[] header = { "Марка", "Год выпуска", "Объём двигателя", "Макс. скорость" };

	@Override
	public int getRowCount()	// возвращает число строк
	{ return data.size(); }

	@Override
	public int getColumnCount()	// возвращает число столбцов
	{ return 4; }
	
	@Override
	public Class<?> getColumnClass(int columnIndex)	// возвращает тип значения столбца
	{
		return getValueAt(0, columnIndex).getClass();
	}
	
	@Override
	public Object getValueAt(int rowIndex, int columnIndex)	// возвращает значение поля таблицы
	{
		Auto element = getRow(rowIndex);
		switch (columnIndex)
		{
			case 0: return element.brand;
			case 1: return element.year;
			case 2: return element.engineVolume;
			case 3: return element.maxSpeed;
		}
		return null;
	}
	
	@Override
	public void setValueAt(Object value, int rowIndex, int columnIndex)	// выполняет изменение данных в ячейке
	{
		Auto element = getRow(rowIndex);
		switch (columnIndex)
		{
			case 0: element.brand = (String)value; break;
			case 1: element.year = (int)value; break;
			case 2: element.engineVolume = (float)value; break;
			case 3: element.maxSpeed = (int)value; break;
		}
	}

	@Override
	public boolean isCellEditable(int rowIndex, int columnIndex)	// узнать возможность редактирования ячейки
	{ return true; }
	
	// Возвращает имя столбца
	public String getColumnName(int columnIndex)
	{
		return header[columnIndex];
	}

	public Auto getRow(int rowIndex)	// возвращает объект по индексу
	{
		int counter = 0;
		for (Auto obj: data)
		{
			if (counter++ == rowIndex)
			{
				return obj;
			}
		}
		return null;
	}

	// Возвращает итератор коллекции
	public Iterator<Auto> getIterator()
	{ return data.iterator(); }

	// Добавляет к таблице объект
	public void addRow(Auto obj)	
	{
		data.add(obj);
		fireTableDataChanged();
	}

	// Добавляет в таблицу объекты коллекции
	public void addRows(Collection<Auto> rows)
	{
		rows.forEach(data::add);
		fireTableDataChanged();
	}
	
	// Удаляет объект по значению поля 1
	public void deleteRow(String brand)	
	{
		Iterator<Auto> iter = data.iterator();
		while (iter.hasNext())
		{
			if (iter.next().brand.equals(brand))
			{
				iter.remove();
				//break;
			}
		}
		fireTableDataChanged();
		return;
	}
	
	// Обновление строки в таблице
	public void updateRow(int rowIndex, Auto obj)
	{
		setValueAt(obj.brand, rowIndex, 0);
		setValueAt(obj.year, rowIndex, 1);
		setValueAt(obj.engineVolume, rowIndex, 2);
		setValueAt(obj.maxSpeed, rowIndex, 3);
		fireTableDataChanged();	
	}

	// Полная очистка таблицы
	public void clearRows()	
	{
		data.clear();
		fireTableDataChanged();
	}
}
