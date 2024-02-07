import java.util.Random;

public class Buffer extends CBuffer
{
	protected double[] bufArray;	// массив для чисел
	protected static final Random random = new Random();	// ГСЧ

	public Buffer(int size)	// конструктор класса
	{
		super(size);
		bufArray = new double[bufSize];
		Generate();
	}

	@Override
	protected void Generate()	// заполнение буфера случайными числами
	{
		for (int i = 0; i < bufSize; ++i)
			bufArray[i] = random.nextDouble();
	}
}
