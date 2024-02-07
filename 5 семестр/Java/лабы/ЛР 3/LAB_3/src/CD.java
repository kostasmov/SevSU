
public class CD implements Comparable<CD>
{
	public final String albumTitle;
	public final String artist;
	public final int tracksCount;
	public final int duration;

	public CD(String albumTitle, String artist, int tracksCount, int duration)
	{
		this.albumTitle = albumTitle;
		this.artist = artist;
		this.tracksCount = tracksCount;
		this.duration = duration;
	}

	@Override
	public int compareTo(CD obj)
	{
		return albumTitle.compareTo(obj.albumTitle);
	}

	@Override
	public String toString()
	{
		return String.format("Альбом: %s. Автор: %s. %d треков (%d мин.)", albumTitle, artist, tracksCount, duration);
	}
}