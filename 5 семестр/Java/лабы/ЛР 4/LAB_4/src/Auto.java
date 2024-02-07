
// Класс для типа информации C по варианту
public class Auto
{
	// Параметры
	public String brand;		// марка
	public int year;			// год выпуска
	public float engineVolume;	// объём двигателя, л.
	public int maxSpeed;		// макс. скорость, км/ч.

	// Передача параметров через конструктор
	public Auto(String brand, int year, float engineVolume, int maxSpeed)
	{
		this.brand = brand;
		this.year = year;
		this.engineVolume = engineVolume;
		this.maxSpeed = maxSpeed;
	}

	@Override
	public String toString()	// представление объекта в виде строки (для csv файла)
	{
		return String.format("%s;%d;%f;%d", brand, year, engineVolume, maxSpeed);
	}

	@Override
	public boolean equals(Object obj)	// сравнение с другим объектом
	{
		if (obj instanceof Auto)
		{
			Auto other = (Auto) obj;
			return brand == other.brand && year == other.year && maxSpeed == other.maxSpeed && engineVolume == other.engineVolume;
		}
		return false;
	}
}
