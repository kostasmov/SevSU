#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

const double taxRate = 0.05;        // ставка НДС
const double discountRate = 0.1;    // % скидки при наличии карты

// КЛАСС ДЛЯ ОБРАБОТКИ ЗАКАЗА
class Order
{
protected:
    vector<double> prices;	// цены товаров в заказе
    bool hasDiscount;       // есть ли скидочная карта?	
	
	double totalPrice;	// цена без налога и скидки
	double discount;	// скидка
	double tax;			// налог
public:
    // конструктор
    Order(vector<double> prices, bool hasDiscount) : prices(prices),
                                                   hasDiscount(hasDiscount){
    	processOrder();
    }
	
    // вывод чека
    void printReceipt() 
	{
		cout << " ----- RECEIPT -----" << endl;
        for (int i = 0; i < prices.size(); i++)
		{
		    cout << " Product " << i << ": " << prices[i] << "$" << endl;
		}
        cout << "-------------------" << endl;	
		cout << left << setw(12) << " SUBTOTAL:" << totalPrice << "$" << endl;
		cout << left << setw(12) << " DISCOUNT:" << discount << "$" << endl;
		cout << left << setw(12) << " TAX:"      << tax << "$" << endl;
		cout << left << setw(12) << " TOTAL:" << totalPrice - discount + tax << "$" << endl;
    }
private:
	// обработка заказа
    void processOrder()
    {
		totalPrice = calculateTotal();
		discount = calculateDiscount(totalPrice);
		tax = calculateTax(totalPrice, discount);
	}
	
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
	Order order({10.0, 20.0, 15.0}, true);
    order.printReceipt();
    
    return 1;
}
