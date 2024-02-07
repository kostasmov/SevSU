import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.ListSelectionModel;
import javax.swing.border.EmptyBorder;

public class jfMyFrame extends JFrame
{
	private static final long serialVersionUID = 26268648356920251L;

	// Используемые компоненты
	private final JPanel contentPane = new JPanel();					// главная (корневая) панель
	private final AutoTableModel tableModel = new AutoTableModel();		// модель табличного представления данных
	private final JTable dataTable = new JTable(tableModel);			// таблица данных
	private final JScrollPane scrollPane = new JScrollPane(dataTable);	// прокручиваемая панель
	
	private final JPanel buttonsPane = new JPanel();	// панель для кнопок
	private final JPanel fieldsPane = new JPanel();		// панель для полей ввода

	// Кнопки
	private final JButton addButton = new JButton("Добавить");
	private final JButton updateButton = new JButton("Изменить");
	private final JButton deleteButton = new JButton("Удалить");
	private final JButton inputButton = new JButton("Загрузить");
	private final JButton outputButton = new JButton("Выгрузить");

	// Подписи полей ввода
	private final JLabel brandFieldLabel = new JLabel("Марка");
	private final JLabel yearFieldLabel = new JLabel("Год выпуска");
	private final JLabel engineVolumeFieldLabel = new JLabel("Объём двигателя");
	private final JLabel maxSpeedFieldLabel = new JLabel("Максимальная скорость");
	
	// Класс управления полями ввода данных
	private final TextFields textFieldGroup = new TextFields();
	
	// Запуск окна приложения
	public static void main(String[] args)
	{
		EventQueue.invokeLater(new Runnable()
		{
			public void run ()
			{
				try
				{
					jfMyFrame frame = new jfMyFrame();
					frame.setVisible(true);
				}
				catch (Exception e)
				{ e.printStackTrace(); }
			}
		});
	}

	// Окно приложения
	public jfMyFrame()
	{
		// Настройки окна приложения
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setTitle("Ведомость автомобилей");
		setBounds(200, 100, 450, 300);

		// Настройки корневой панели
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		contentPane.setLayout(new BorderLayout(0, 0));
		setContentPane(contentPane);

		// Настройки прокручеваемой панели
		contentPane.add(scrollPane, BorderLayout.CENTER);

		// Панель для кнопок
		contentPane.add(buttonsPane, BorderLayout.EAST);
		buttonsPane.setLayout(new BoxLayout(buttonsPane, BoxLayout.Y_AXIS));
		
		buttonsPane.add(addButton);
		buttonsPane.add(updateButton);
		buttonsPane.add(deleteButton);
		buttonsPane.add(inputButton);
		buttonsPane.add(outputButton);

		// Панель с полями ввода
		fieldsPane.setLayout(new GridLayout(0, 2));
		contentPane.add(fieldsPane, BorderLayout.NORTH);
		
		fieldsPane.add(brandFieldLabel);
		fieldsPane.add(textFieldGroup.brandField);
		fieldsPane.add(yearFieldLabel);
		fieldsPane.add(textFieldGroup.yearField);
		fieldsPane.add(engineVolumeFieldLabel);
		fieldsPane.add(textFieldGroup.engineVolumeField);
		fieldsPane.add(maxSpeedFieldLabel);
		fieldsPane.add(textFieldGroup.maxSpeedField);

		// Настройка таблицы данных
		dataTable.getSelectionModel().setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

		// Действия при нажатии кнопки "Добавить"
		addButton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				try
				{
					tableModel.addRow(textFieldGroup.getObject());
				}
				catch (NumberFormatException ex)
				{
					JOptionPane.showMessageDialog(null, "ОШИБКА: Данные заполнены неверно");
				}
			}
		});
		
		// Действия при нажатии кнопки "Изменить"
		updateButton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				try
				{
					if (dataTable.getSelectedRow() >= 0)
					{
						tableModel.updateRow(dataTable.getSelectedRow(), textFieldGroup.getObject());
					}
					else
					{
						JOptionPane.showMessageDialog(null, "ОШИБКА: Не выбрана строка");
					}
				}
				catch (NumberFormatException ex)
				{
					JOptionPane.showMessageDialog(null, "ОШИБКА: Данные заполнены неверно");
				}
			}
		});
		
		// Действия при нажатии кнопки "Удалить"
		deleteButton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				tableModel.deleteRow(textFieldGroup.brandField.getText());
			}
		});
		
		// Действия при нажатии кнопки "Загрузить"
		inputButton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				try
				{
					File file = new FileChooser().getReadFile();
					if (file != null)
					{
						tableModel.clearRows();
						tableModel.addRows((new FileManager(file)).readSet());
					}
				}
				catch (Exception ex)																																																							
				{
					JOptionPane.showMessageDialog(null, ex.getMessage());
				}
			}
		});
		
		// Действия при нажатии кнопки "Выгрузить"
		outputButton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				try
				{
					File file = new FileChooser().getSaveFile();
					if (file != null)
					{
						new FileManager(file).writeSet(tableModel.getIterator());
					}
				}
				catch (Exception ex)
				{
					JOptionPane.showMessageDialog(null, ex.getMessage());
				}
			}
		});
		
		// Действия при нажатии на строку таблицы
		dataTable.addMouseListener(new MouseAdapter()
		{
			@Override
			public void mouseClicked(MouseEvent event)
			{
				textFieldGroup.fillTextFields(tableModel.getRow(dataTable.getSelectedRow()));
			}
		});
	}
}
