#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;


// КЛАСС ЦЕНОВОЙ ПОЛИТИКИ
class PricePolicy 
{
	static constexpr double taxRate = 0.05;		// ставка НДС
	static constexpr double discountRate = 0.1;	// % скидки при наличии карты
public:
	static double getTaxRate() { return taxRate; }
	static double getDiscountRate() { return discountRate; }
};


// КЛАСС ДЛЯ КАССИРОВ
class Cashier
{
public:
	string f_name;	// имя
	string l_name;	// фамилия
	
	Cashier(string f_name, string l_name) : f_name(f_name), 
											l_name(l_name) {}
};


// ГРАНИЧНЫЙ ОБЪЕКТ ДЛЯ ДАННЫХ ЧЕКА 
class OrderData { 
public: 	
	double totalPrice;	// цена без налога и скидки
	double discount;	// скидка
	double tax;			// налог
	Cashier* cashier;	// кассир
	
	OrderData(double totalPrice=0, double discount=0, double tax=0, 
				Cashier* cashier=nullptr)
	   : totalPrice(totalPrice), 
		 discount(discount), 
		 tax(tax), 
		 cashier(cashier) {} 
};


// КЛАСС ДЛЯ ВЫВОДА ЧЕКА
class Printer 
{
public:
	// вывод чека
	static void printReceipt(vector<double> prices, OrderData order)	
	{
		const string separator = " ------------------- ";
		
		cout << " ----- RECEIPT ----- " << endl;
		
        for (int i = 0; i < prices.size(); i++)
		{
			printReceiptLine("Product " + to_string(i+1), prices[i]);
		}
		
        cout << separator << endl;
			
        printReceiptLine("SUBTOTAL", order.totalPrice);
        printReceiptLine("DISCOUNT", order.discount);
        printReceiptLine("TAX", order.tax);
        printReceiptLine("TOTAL", order.totalPrice - order.discount + order.tax);
        
        cout << separator << endl;
        
        printReceiptLine("Cashier", order.cashier->f_name + " " + order.cashier->l_name);
    }
private:    
	static void printReceiptLine(string label, double value, char sign='$') 
	{
		cout << left << setw(12) << " " + label + ": " << value << sign << endl;
	}
	
	static void printReceiptLine(string label, string value) {
        cout << left << setw(12) << " " + label + ": " << value << endl;
    }
};

// КЛАСС ДЛЯ ОБРАБОТКИ ЗАКАЗА
class Order
{
protected:
    vector<double> prices;	// цены товаров в заказе
    bool hasDiscount;       // есть ли скидочная карта?	

	OrderData data;
public:
    // конструктор
    Order(vector<double> prices, bool hasDiscount, Cashier cashier)
        : prices(prices),
          hasDiscount(hasDiscount),
          data()
    {
    	data.cashier = &cashier;
		data.totalPrice = calculateTotal();
		data.discount = calculateDiscount(data.totalPrice); 
		data.tax = calculateTax(data.totalPrice, data.discount);
	}
	
	// вывод чека
    void printReceipt() 
	{
		Printer :: printReceipt(prices, data);
    }
private:	
	// подсчёт суммы заказа
	double calculateTotal() 
	{
        double total = 0.0;
        for (double price : prices) { total += price; }
        return total;
    }

	// подсчёт скидки (при наличии)
    double calculateDiscount(double total) 
	{
		double discountRate = PricePolicy::getDiscountRate();
        return hasDiscount ? (total * discountRate) : 0;
    }

	// подсчёт налога (с учётом скидки)
    double calculateTax(double total, double discnt) 
	{
		double taxRate = PricePolicy::getTaxRate();
        return (total - discnt) * taxRate;
    }
};


int main()
{
	Cashier cashier = Cashier("Zoreslav", "Nikiforov");
	
	Order order({10.0, 20.0, 15.0}, true, cashier);
    order.printReceipt();
    
    return 0;
}