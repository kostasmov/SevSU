#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

const double taxRate = 0.05;		// ставка НДС
const double discountRate = 0.1;	// % скидки при наличии карты

// КОД ПРОГРАММЫ
int main()
{
    vector<double> prices = {10.0, 20.0, 15.0};	// цены товаров в заказе
	bool hasDiscount = true;					// есть ли скидочная карта?
	
	// вывод чека
	cout << " ------ RECEIPT ------" << endl;
    for (int i = 0; i < prices.size(); i++)
	{
	    cout << " Product " << i + 1 << ": " << prices[i] << "$" << endl;
	}
	cout << " ---------------------" << endl;
	
	// вывод суммы заказа (без налога и скидки)
	double totalPrice = 0.0;
	for (double price : prices)
    {
        totalPrice += price;
    }
	cout << left << setw(12) << " SUBTOTAL:" << totalPrice << "$" << endl;
	
	// вывод скидки
	cout << left << setw(12) << " DISCOUNT:" << (hasDiscount ? (totalPrice * discountRate) : 0) << "$" << endl;
	totalPrice -= hasDiscount ? (totalPrice * discountRate) : 0;
	
	// вывод налога 
    cout << left << setw(12) << " TAX:" << totalPrice * taxRate << "$" << endl;
    totalPrice += totalPrice * taxRate;	
    
    // итоговая цена заказа
	cout << left << setw(12) << " TOTAL:" << totalPrice << "$" << endl;
    
    return 0;
}
