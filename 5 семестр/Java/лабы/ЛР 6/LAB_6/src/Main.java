import java.util.Random; 
import static java.lang.Math.abs;

public class Main
{
	static final int N = 10000;						// размер массивов
	static final boolean PRINT_SEQUENTLY = true;	// способ вывода (true - поэлементно)
    
	// Сортировка массива методом пузырька
	public static void bubbleSort(int[] arr)
	{
	    for (int i = 0; i < arr.length - 1; i++)
	    {
	        for (int j = 0; j < arr.length - i - 1; j++)
	        {
	            if (arr[j] < arr[j + 1])
	            {
	                int temp = arr[j];
	                arr[j] = arr[j + 1];
	                arr[j + 1] = temp;
	            }
	        }
	    }
	}
	
	// Сортировка и вывод массива одним вызовом println()
    public static void printSorted(int[] arr)
    {   
    	bubbleSort(arr);

		String line = Thread.currentThread().getName() + ": "; 
		for (int i = 0; i < N; i++)
		{
			line += arr[i] + " ";
		}
		System.out.println(line);
	}
    
    // Сортировка и вывод массива поэлементно
    public static void printSortedSequently(int[] arr)
    { 
    	bubbleSort(arr);
  
        System.out.println("**************************************************");
        for(int i = 0; i < N/100; i++)
        { 
            System.out.print(Thread.currentThread().getName() + ": "); 
            for (int j = 0; j < 100; j++)
            {
                System.out.print(arr[i*100 + j] + " ");
            }
            System.out.println();
        }
        System.out.println("**************************************************");
    }
    
    // Главный метод - выполнение программы
    public static void main(String[] args) throws InterruptedException
    {
    	// Создание массивов из N целых чисел
        int[] arr_1 = new int[N], arr_2 = new int[N], 
        		arr_3 = new int[N];
        
        // Заполнение массивов случайными числами [0; 99]
        Random rand = new Random(); 
        for (int i = 0; i < N; i++)
        {
        	arr_1[i] = abs(rand.nextInt() % 100); 
          	arr_2[i] = abs(rand.nextInt() % 100); 
          	arr_3[i] = abs(rand.nextInt() % 100);
        }
        
        // Определение потоков обработки массивов
        Thread thread_1, thread_2, thread_3; 
        if (!PRINT_SEQUENTLY)	// вывод одним вызовом
        {
        	thread_1 = new Thread(() -> printSorted(arr_1));
        	thread_2 = new Thread(() -> printSorted(arr_2)); 
            thread_3 = new Thread(() -> printSorted(arr_3));
        }
        else					// вывод поэлементно
        {
            thread_1 = new Thread(() -> printSortedSequently(arr_1));
            thread_2 = new Thread(() -> printSortedSequently(arr_2));
            thread_3 = new Thread(() -> printSortedSequently(arr_3));
        }
        
        // Имена потоков
        thread_1.setName("Thread_1"); 
        thread_2.setName("Thread_2"); 
        thread_3.setName("Thread_3");
        
        // Приоритеты потоков
        thread_1.setPriority(8); 
        thread_2.setPriority(5); 
        thread_3.setPriority(1);
        
        // Запуск потоков
      	thread_1.start(); 
      	thread_2.start(); 
      	thread_3.start();
    }
}
