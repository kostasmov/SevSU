
public abstract class CBuffer
{
	private static int bufCount = 0;	// количество буферов

	protected final int bufID;		// идентификатор
	protected final int bufSize;	// размер буфера

	public CBuffer(int count)	// конструктор класса
	{
		bufID = ++bufCount;
		bufSize = count;
	}

	public final int GetBufID()
	{ return bufID; }

	public final int GetBufCount()
	{ return bufCount; }

	protected abstract void Generate();
}
