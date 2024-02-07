package application;

import java.io.File;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.FileReader;

import javafx.collections.FXCollections;
import javafx.collections.ListChangeListener;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.converter.DoubleStringConverter;
import javafx.util.converter.IntegerStringConverter;

// Класс управления компонентами приложения
public class Controller
{
	// Таблица и её колонки
	@FXML private TableView<Auto> table;
	private ObservableList<Auto> data = FXCollections.observableArrayList();
	@FXML private TableColumn<Auto, String> colBrand;
	@FXML private TableColumn<Auto, Integer> colYear;
	@FXML private TableColumn<Auto, Double> colEngineVolume;
	@FXML private TableColumn<Auto, Integer> colMaxSpeed;
	
	// Кнопки
	@FXML private Button btnAdd, btnLoad, btnSave, btnDelete;
	
	// Текстовые поля ввода
	@FXML private TextField txtBrand, txtYear, txtEngineVolume, txtMaxSpeed; 
	
	// Круговая диаграмма
	@FXML private PieChart chart;
	private ObservableList<PieChart.Data> pcData = FXCollections.observableArrayList();
	
	// Компонент выбора файла
	private FileChooser fileChooser = new FileChooser();
	
	// Начальные настройки компонентов приложения
	@FXML private void initialize()
	{
		fileChooser.setInitialDirectory(
				new File("C:\\Users\\kosta\\Documents\\Учёба\\СДЕЛАНО\\5 семестр\\Java"));
		table.setEditable(true);
		table.setItems(data);

		data.addListener(new ListChangeListener<Auto>()
		{
			@Override public void onChanged(
				javafx.collections.ListChangeListener.Change<? extends Auto> arg0) {
					updateChart();
				}
		});
		
		setColBrand();
		setColYear();
		setColEngineVolume();
		setColMaxSpeed();
	}
	
	// Настройка колонки "Марка"
	private void setColBrand()
	{
		colBrand.setCellValueFactory(new PropertyValueFactory<Auto, String>("brand"));
		colBrand.setCellFactory(TextFieldTableCell.forTableColumn());
		colBrand.setOnEditCommit(event -> 
		{
			String brand = event.getNewValue();
			if (brand.isEmpty())
			{ 
				showAlert("Пустое поле", "Заполните поле \"Марка\""); 
			}
			else event.getRowValue().setBrand(brand);
			updateChart();
		});
	}
	
	// Настройка колонки "Год выпуска"
	private void setColYear()
	{
		colYear.setCellValueFactory(new PropertyValueFactory<Auto, Integer>("year"));
		colYear.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()
		{
			@Override public Integer fromString(String value)
			{
		        try
		        {
		            return Integer.parseInt(value);
		        }
		        catch (NumberFormatException e)
		        {
		            return null;
		        }
		    }
		}));
		
		colYear.setOnEditCommit(event -> 
		{
			try
			{
				Integer year = event.getNewValue();
				if (year == null) { throw new Exception(); }
				event.getRowValue().setYear(year);	
			}
			catch (Exception e)
			{
				showAlert("Ошибка формата", "Введите корректное значение года выпуска.");
			}
			
			updateChart();
		});
	}
	
	// Настройка колонки "Объём двигателя"
	private void setColEngineVolume()
	{
		colEngineVolume.setCellValueFactory(new PropertyValueFactory<Auto, Double>("engineVolume"));
		colEngineVolume.setCellFactory(TextFieldTableCell.forTableColumn(new DoubleStringConverter()
		{
			@Override public Double fromString(String value)
			{
		        try
		        {
		            return Double.parseDouble(value);
		        }
		        catch (NumberFormatException e)
		        {
		            return null;
		        }
		    }
		}));
		
		colEngineVolume.setOnEditCommit(event -> 
		{
			try
			{
				Double volume = event.getNewValue();
				if (volume == null) { throw new Exception(); }
				event.getRowValue().setEngineVolume(volume);
			}
			catch (Exception e)
			{
				showAlert("Ошибка формата","Введите корректное значение объёма двигателя.");
			}
			
			updateChart();
		});
	}
	
	// Настройка колонки "Макс. скорость"
	private void setColMaxSpeed()
	{
		colMaxSpeed.setCellValueFactory(new PropertyValueFactory<Auto, Integer>("maxSpeed"));
		colMaxSpeed.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()
		{
			@Override public Integer fromString(String value)
			{
		        try
		        {
		            return Integer.parseInt(value);
		        }
		        catch (NumberFormatException e)
		        {
		            return null;
		        }
		    }
		}));
		
		colMaxSpeed.setOnEditCommit(event -> 
		{
			try
			{
				Integer maxSpeed = event.getNewValue();
				if (maxSpeed == null) { throw new Exception(); }
				event.getRowValue().setMaxSpeed(maxSpeed);	
			}
			catch(Exception e)
			{
				showAlert("Ошибка формата", "Введите корректное значение скорости.");
			}
			
			updateChart();
		});
	}
		
	// Вывод окна с сообщением
	private void showAlert(String header, String text)
	{
		Alert alert = new Alert(Alert.AlertType.ERROR);
		alert.setTitle("Ошибка");
		alert.setHeaderText(header);
		alert.setContentText(text);
		alert.show();
	}
	
	// Обновление круговой диаграммы
	public void updateChart()
	{
		int i;
		pcData.clear();
		
		for (i = 0; i < data.size(); i++)
		{
			pcData.add(new PieChart.Data(data.get(i).getBrand().toString(), data.get(i).getEngineVolume()));
		}
		
		chart.setData(pcData);
	}
	
	// Действия для кнопки "Добавить запись"
	@FXML public void addEntry()
	{
		String brand = txtBrand.getText(),
			   year = txtYear.getText(),
			   engineVolume = txtEngineVolume.getText(),
			   maxSpeed = txtMaxSpeed.getText();
		
		int yearValue, speedValue;
		double volumeValue;
		
		if (brand.isEmpty() || year.isEmpty() || engineVolume.isEmpty() || maxSpeed.isEmpty())
		{
			showAlert("Запись не создана", "Заполните все поля.");
		}
		else
		{		
			try { yearValue = Integer.valueOf(year); }
			catch (NumberFormatException e)
			{
				showAlert("Ошибка формата", "Введите корректное значение года выпуска.");
				return;
			}
			
			try { volumeValue = Double.valueOf(engineVolume); }
			catch (NumberFormatException e)
			{
				showAlert("Ошибка формата", "Введите корректное значение объёма двигателя.");
				return;
			}
			
			try { speedValue = Integer.valueOf(maxSpeed); }
			catch (NumberFormatException e)
			{
				showAlert("Ошибка формата", "Введите корректное значение скорости.");
				return;
			}
			
			data.add(new Auto(brand, yearValue, volumeValue, speedValue));
			
			txtBrand.clear(); 
			txtYear.clear(); 
			txtEngineVolume.clear(); 
			txtMaxSpeed.clear();
			
			updateChart();
		} 
	}
	
	// Действия для кнопки "Удалить запись"
	@FXML public void deleteEntry() 
	{
		Auto car = table.getSelectionModel().getSelectedItem();
		if (car != null)
		{
			data.remove(car);
			updateChart();
		}
	}
	
	// Действия для кнопки "Загрузка таблицы"
	@FXML public void loadData()
	{
		fileChooser.setTitle("Загрузка");
		File file = fileChooser.showOpenDialog(new Stage());
		if (file != null)
		{
			try (BufferedReader reader = new BufferedReader(new FileReader(file)))
			{
				ObservableList<Auto> list = FXCollections.observableArrayList();
				String line;
				
				while ((line = reader.readLine()) != null)
				{
					String[] parts = line.split(";");
					
					String brand = parts[0];
					int year = Integer.parseInt(parts[1]);
					double pageCount = Double.parseDouble(parts[2].replace(",", "."));
					int speed = Integer.parseInt(parts[3]);
					
					list.add(new Auto(brand, year, pageCount, speed));
				}
				
				data.setAll(list);
				updateChart();
			}
			catch (Exception e)
			{
				showAlert("Ошибка чтения", "Не удалось прочесть данные.");
			}
		}
	}
	
	// Действия для кнопки "Запись таблицы"
	@FXML public void saveData()
	{
	    fileChooser.setTitle("Сохранение");
	    File file = fileChooser.showSaveDialog(new Stage());
	    
	    if (file != null)
	    {
	        try
	        {
	            BufferedWriter writer = new BufferedWriter(new FileWriter(file));
	            ObservableList<Auto> list = data;
	         
	            for (Auto car: list)
	            {	writer.write(car.toString() + '\n');	}
	            
	            writer.close();
	            updateChart();
	        }
	        catch (Exception e)
	        {
	            showAlert("Ошибка сохранения", "Не удалось сохранить записи в файле.");
	        }
	    }
	}
}