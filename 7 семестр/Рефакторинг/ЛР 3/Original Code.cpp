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
};                              


// Обработка фигуры
void processShape(Rectangle frame, Shape* s) { 
	bool stop = false;
	
	if (s == nullptr) { 
		cout << "Error: Null shape" << endl; 
		stop = true;
	} 
	
	if (!stop) { 
		string s_type = s->getType();
	
		if (s_type == "circle") { 
			double area = pow(s->getWidth()/2, 2) * M_PI;
			cout << "Area of circle: " << area << endl; 
			if ((s->getHeight() <= frame.getHeight()) && (s->getWidth() <= frame.getWidth())) {
				cout << "Circle fit!" << endl << endl;
			} else { cout << "Circle not fit!" << endl << endl; }
		} else if (s_type == "rectangle") { 
			double area = s->getWidth() * s->getHeight();
			cout << "Area of rectangle: " << area << endl; 
			if ((s->getHeight() <= frame.getHeight()) && (s->getWidth() <= frame.getWidth())) {
				cout << "Rectangle fit!" << endl << endl;
			} else { cout << "Rectangle not fit!" << endl << endl; }
		} else { 
			cout << "Error: Shape undefined" << endl; 
		} 
	} 
} 


// КОД ПРОГРАММЫ
int main() { 
	const Rectangle block(20, 20);

	Shape* s1 = new Circle(10);
	Shape* s2 = new Rectangle(5, 25);
	Shape* s3 = nullptr;
	
	processShape(block, s1);
	processShape(block, s2);
	processShape(block, s3);
	
	delete s1;
	delete s2;
	
	return 0; 
}