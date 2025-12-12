#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

const double taxRate = 0.05;		// ставка НДС
const double discountRate = 0.1;	// % скидки при наличии карты


// КЛАСС ДЛЯ ФИНАНСОВЫХ РАССЧЁТОВ
class PriceCalculator {
public:
    double static calculateTotal(const vector<double>& prices) {
        double total = 0.0;
        for (double price : prices) total += price;
        return total;
    }

    double static calculateDiscount(double total, bool hasDiscount) {
        return hasDiscount ? (total * discountRate) : 0;
    }

    double static calculateTax(double total, double discount) {
        return (total - discount) * taxRate;
    }
};


// КЛАСС ДЛЯ ОБРАБОТКИ ЗАКАЗА
class Order
{
protected:
    vector<double> prices;	// цены товаров в заказе
    bool hasDiscount;       // есть ли скидочная карта?	
    
    string cashier_fname;	// имя кассира
    string cashier_lname;	// фамилия кассира
	
	double totalPrice;	// цена без налога и скидки
	double discount;	// скидка
	double tax;			// налог
public:
    // конструктор
    Order(vector<double> prices, bool hasDiscount, string f_name, string l_name)
        : prices(prices),
          hasDiscount(hasDiscount),
          cashier_fname(f_name),
          cashier_lname(l_name)
          
    {
        totalPrice = PriceCalculator::calculateTotal(prices);
		discount = PriceCalculator::calculateDiscount(totalPrice, hasDiscount);
		tax = PriceCalculator::calculateTax(totalPrice, discount);
	}
	
	// вывод чека
    void printReceipt() 
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
        
        printReceiptLine("Cashier", cashier_fname + ' ' + cashier_lname);
    }
private:
	void printReceiptLine(string label, double value, char sign='$') 
	{
		cout << left << setw(12) << " " + label + ": " << value << sign << endl;
	}
	
	void printReceiptLine(string label, string value) {
        cout << left << setw(12) << " " + label + ": " << value << endl;
    }
};

// КОД ПРОГРАММЫ
int main()
{
	Order order({10.0, 20.0, 15.0}, true, "Zoreslav", "Nikiforov");
    order.printReceipt();
    
    return 1;
}