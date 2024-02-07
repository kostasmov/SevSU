import javax.swing.JTextField;

// Класс управления текстовыми полями ввода данных
public class TextFields
{
	// Текстовые поля
	public final JTextField brandField = new JTextField();
	public final JTextField yearField = new JTextField();
	public final JTextField engineVolumeField = new JTextField();
	public final JTextField maxSpeedField = new JTextField();

	// Построение объекта Auto по значениям полей ввода
	public Auto getObject()
	{
		Auto obj = new Auto(brandField.getText(), Integer.parseInt(yearField.getText()), 
				Float.parseFloat(engineVolumeField.getText()), Integer.parseInt(maxSpeedField.getText()));
		return obj;
	}

	// Заполнение текстовых полей значениями свойств объекта
	public void fillTextFields(Auto obj)
	{
		brandField.setText(obj.brand);
		yearField.setText(Integer.toString(obj.year));
		engineVolumeField.setText(Float.toString(obj.engineVolume));
		maxSpeedField.setText(Integer.toString(obj.maxSpeed));
	}

	// Очистка всех текстовх полей
	public void clearAll()
	{
		brandField.setText("");
		yearField.setText("");
		engineVolumeField.setText("");
		maxSpeedField.setText("");
	}
}
