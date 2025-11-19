#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

// КЛАСС ДЛЯ ОБРАБОТКИ ЗАКАЗА
class Order
{
private:
    vector<double> items;   // цены заказанных продуктов
    bool hasDiscount;       // наличие скидочной карты
    double taxRate;         // налоговая ставка

    double discountRate = 0.1;  // скидка 10%
public:
    // конструктор
    Order(vector<double> items, bool hasDiscount, double taxRate) : items(items),
                                                                    hasDiscount(hasDiscount),
                                                                    taxRate(taxRate)
    {}

    // обработка заказа
    void processOrder()
    {
        double total = 0.0;		// сумма заказа
        double tax = 0.0;		// сумма налога
        double discount = 0.0;	// сумма скидки

        // подсчёт суммы заказа
        for (double price : items)
        {
            total += price;
        }

        // подсчёт скидки (при наличии)
        if (hasDiscount)
        {
            discount = total * discountRate;
        }

        // подсчёт налога (с учётом скидки!)
        tax = (total - discount) * taxRate;

        // вывод чека
        cout << "----- RECEIPT -----" << endl;
        for (int i = 0; i < items.size(); i++)
		{
		    cout << "Product " << i + 1 << ": " << items[i] << "$" << endl;
		}
        cout << "-------------------" << endl;	
		cout << left << setw(12) << "SUBTOTAL:" << total    			  << "$" << endl;	// цена без налога и скидки
		cout << left << setw(12) << "TAX:"      << tax                    << "$" << endl;	// налог
		cout << left << setw(12) << "DISCOUNT:" << discount               << "$" << endl;	// скидка
		cout << left << setw(12) << "TOTAL:"    << total + tax - discount << "$" << endl;	// итоговая цена заказа
    }
};

// КОД ПРОГРАММЫ
int main()
{
    Order order({10.0, 20.0, 15.0}, true, 0.05);
    order.processOrder();
    return 0;
}
