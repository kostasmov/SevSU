import java.io.IOException;

public class Lab2Java
{
	static final int L = 50, N = 5;

	public static void main(String[] args)
	{
		for (int i = 0; i < N; i++)
		{
			Buffer1 buffer = new Buffer1(L);
			buffer.PrintInfo();
			buffer.PrintFirstN(10);
			buffer.Max();
			buffer.Min();
			buffer.Sort();
			buffer.PrintLastN(10);
			try
			{
				buffer.SaveOneLine("output" + buffer.GetBufID() + ".txt");
			}
			catch (IOException e)
			{
				System.err.println(e.getMessage());
			}
		}
	}
}
