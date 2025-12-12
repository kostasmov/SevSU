#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

const double taxRate = 0.05;		// ставка НДС
const double discountRate = 0.1;	// % скидки при наличии карты

// КЛАСС ДЛЯ КАССИРОВ
class Cashier
{
	string f_name;
	string l_name;
public:
	Cashier(string f_name, string l_name) : f_name(f_name), 
											l_name(l_name) {}
	
	string getFullName() {
		return f_name + ' ' + l_name;
	}
};

// КЛАСС ДЛЯ ВЫВОДА ЧЕКА
class Printer 
{
public:
	// вывод чека
	static void printReceipt(vector<double> prices, double totalPrice, 
							double discount, double tax,
							string cashier_name)	
	{
		const string separator = " ------------------- ";
		
		cout << " ----- RECEIPT ----- " << endl;
		
        for (int i = 0; i < prices.size(); i++)
		{
		    printReceiptLine("Product " + to_string(i+1), prices[i]);
		}
		
        cout << separator << endl;
			
        printReceiptLine("SUBTOTAL", totalPrice);
        printReceiptLine("DISCOUNT", discount);
        printReceiptLine("TAX", tax);
        printReceiptLine("TOTAL", totalPrice - discount + tax);
        
        cout << separator << endl;
        
        printReceiptLine("Cashier", cashier_name);
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
    
    Cashier cashier;	// кассир
	
	double totalPrice;	// цена без налога и скидки
	double discount;	// скидка
	double tax;			// налог
public:
    // конструктор
    Order(vector<double> prices, bool hasDiscount, Cashier cashier)
        : prices(prices),
          hasDiscount(hasDiscount),
          cashier(cashier)
    {
		totalPrice = calculateTotal();
		discount = calculateDiscount(totalPrice);
		tax = calculateTax(totalPrice, discount);
	}
	
	// вывод чека
    void printReceipt() 
	{
		Printer :: printReceipt(prices, totalPrice, discount, tax, cashier.getFullName());
    }
private:
	// подсчёт суммы заказа
	double calculateTotal() 
	{
        double total = 0.0;
        for (double price : prices) 
		{
            total += price;
        }
        return total;
    }

	// подсчёт скидки (при наличии)
    double calculateDiscount(double total) 
	{
        return hasDiscount ? (total * discountRate) : 0;
    }

	// подсчёт налога (с учётом скидки)
    double calculateTax(double total, double discount) 
	{
        return (total - discount) * taxRate;
    }
};

// КОД ПРОГРАММЫ
int main()
{
	Cashier cashier = Cashier("Zoreslav", "Nikiforov");
	
	Order order({10.0, 20.0, 15.0}, true, cashier);
    order.printReceipt();
    
    return 1;
}