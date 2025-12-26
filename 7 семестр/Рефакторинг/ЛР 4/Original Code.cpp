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
	double getTaxRate() { return taxRate; }
	double getDiscountRate() { return discountRate; }
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

// КЛАСС ДЛЯ ВЫВОДА ЧЕКА
class Printer 
{
public:
	// вывод чека
	static void printr(vector<double> prices, double totalPrice, 
							double discount, double tax,
							string cashier_first_name, string cashier_last_name)	
	{
		const string separator = " ------------------- ";
		
		cout << " ----- RECEIPT ----- " << endl;
		
        for (int i = 0; i < prices.size(); i++)
		{
		    printl_num("Product " + to_string(i+1), prices[i]);
		}
		
        cout << separator << endl;
			
        printl_num("SUBTOTAL", totalPrice);
        printl_num("DISCOUNT", discount);
        printl_num("TAX", tax);
        printl_num("TOTAL", totalPrice - discount + tax);
        
        cout << separator << endl;
        
        printl_str("Cashier", cashier_first_name + " " + cashier_last_name);
    }
    
	static void printl_num(string label, double value, char sign='$') 
	{
		cout << left << setw(12) << " " + label + ": " << value << sign << endl;
	}
	
	static void printl_str(string label, string value) {
        cout << left << setw(12) << " " + label + ": " << value << endl;
    }
};


// КЛАСС ДЛЯ ОБРАБОТКИ ЗАКАЗА
class Order
{
protected:
    vector<double> prices;	// цены товаров в заказе
    bool hasDiscount;       // есть ли скидочная карта?	
    Cashier cashier;		// кассир
	
	double totalPrice;	// цена без налога и скидки
	double discount;	// скидка
	double tax;			// налог
	
	double taxRate;			// ставка НДС
	double discountRate;	// % скидки при наличии карты
public:
    // конструктор
    Order(vector<double> prices, bool hasDiscount, Cashier cashier, double tRate, double dRate)
        : prices(prices),
          hasDiscount(hasDiscount),
          cashier(cashier),
          taxRate(tRate),
          discountRate(dRate)
    {
		setTotalPrice(calculateTotal());
		setDiscount(calculateDiscount(totalPrice)); 
		setTax(calculateTax(totalPrice, discount));
	}
	
	// вывод чека
    void printReceipt() 
	{
		Printer :: printr(prices, totalPrice, discount, tax, cashier.f_name, cashier.l_name);
    }
    
    // установка значений через метод
    void setTotalPrice(double total) { totalPrice = total; }
	void setDiscount(double new_disc) { discount = new_disc; }
	void setTax(double new_tax) { tax = new_tax; }

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
        return hasDiscount ? (total * discountRate) : 0;
    }

	// подсчёт налога (с учётом скидки)
    double calculateTax(double total, double discnt) 
	{
		return (total - discnt) * taxRate;
    }
};

// КОД ПРОГРАММЫ
int main()
{
	PricePolicy price_info;
	
	Cashier cashier = Cashier("Zoreslav", "Nikiforov");
	
	Order order({10.0, 20.0, 15.0}, true, cashier, 
				price_info.getTaxRate(), price_info.getDiscountRate());
    order.printReceipt();
    
    return 0;
}