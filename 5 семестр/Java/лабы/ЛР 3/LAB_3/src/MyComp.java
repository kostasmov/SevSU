import java.util.Comparator;

class MyComp implements Comparator<CD>
{
	public int compare(CD a, CD b)
	{
		return b.albumTitle.compareTo(a.albumTitle);
	}
}
