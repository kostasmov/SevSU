#include <iostream>
#include <string>
#include <cmath>

using namespace std; 

// Абстрактный класс ФИГУРА (форма)
class Shape 
{ 
public: 
	virtual ~Shape() = default;
	
	virtual string getType() = 0;	// тип
	virtual double getWidth() = 0;	// ширина
	virtual double getHeight() = 0;	// высота
	virtual double getArea() = 0;	// площадь
};

// Класс ОКРУЖНОСТЬ
class Circle : public Shape 
{ 
	const string type = "circle";
	double r;	// радиус
public: 
	Circle(double radius) : r(radius) {} 
	
	string getType() { return type; }
	double getWidth() { return 2 * r; }
	double getHeight() { return 2 * r; }
	double getArea() { return M_PI * pow(r, 2); }
};


// Класс ПРЯМОУГОЛЬНИК
class Rectangle : public Shape 
{ 	
	const string type = "rectangle";
	double l;	// длина
	double h;	// высота
public: 
	Rectangle(double length, double height) : l(length), h(height) {} 
	
	string getType() { return type; }
	double getWidth() { return l; }
	double getHeight() { return h; }
	double getArea() { return l * h; }
};

// NULL-Форма
class NullShape : public Shape 
{ 
public: 
	string getType() { return "undefined"; } 
	double getWidth() { return 0; } 
	double getHeight() { return 0; } 
	double getArea() { return 0; }
};

// Обработка фигуры
void processShape(Rectangle frame, Shape* s) 
{
	string s_type = s->getType();

	if (s_type != "circle" && s_type != "rectangle") { 
		cout << "Error: Shape undefined" << endl; 
		return;
	}

	cout << "Area of " << s->getType() << ": " << s->getArea() << endl; 
	
	if ((s->getHeight() <= frame.getHeight()) && (s->getWidth() <= frame.getWidth())) {
		cout << "Shape fit!" << endl << endl;
	} else { cout << "Shape not fit!" << endl << endl; }
}

// КОД ПРОГРАММЫ
int main() { 
	const Rectangle block(20, 20);

	Shape* s1 = new Circle(10);
	Shape* s2 = new Rectangle(5, 25);
	Shape* s3 = new NullShape();;
	
	processShape(block, s1);
	processShape(block, s2);
	processShape(block, s3);
	
	delete s1;
	delete s2;
	
	return 0; 
}