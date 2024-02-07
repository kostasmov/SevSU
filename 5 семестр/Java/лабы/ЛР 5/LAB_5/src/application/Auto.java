package application;

import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;

//Класс для типа информации T по варианту
public class Auto
{
	// Параметры
	private SimpleStringProperty brand;			// марка
	private SimpleIntegerProperty year;			// год выпуска
	private SimpleDoubleProperty engineVolume;	// объём двигателя, л.
	private SimpleIntegerProperty maxSpeed;		// макс. скорость, км/ч.

	// Передача параметров через конструктор
	public Auto(String brand, int year, double engineVolume, int maxSpeed)
	{
		this.brand = new SimpleStringProperty(brand);
		this.year = new SimpleIntegerProperty(year);
		this.engineVolume = new SimpleDoubleProperty(engineVolume);
		this.maxSpeed = new SimpleIntegerProperty(maxSpeed);
	}
	
	// Методы получения параметров (getters)
	public String getBrand()
	{	return brand.get();	}

	public int getYear()
	{	return year.get();	}

	public double getEngineVolume()
	{	return engineVolume.get();	}

	public int getMaxSpeed()
	{	return maxSpeed.get();	}
	
	
	// Методы изменения параметров (setters)
	public void setBrand(String brand)
	{	this.brand.set(brand);	}

	public void setYear(int year)
	{	this.year.set(year);	}

	public void setEngineVolume(double volume)
	{	this.engineVolume.set(volume);	}

	public void setMaxSpeed(int speed)
	{	this.maxSpeed.set(speed);	}
	
	
	// Представление объекта в виде строки (для csv файла)
	@Override public String toString()
	{
		return String.format("%s;%d;%f;%d", 
				brand.get(), year.get(), engineVolume.get(), maxSpeed.get());
	}
}
