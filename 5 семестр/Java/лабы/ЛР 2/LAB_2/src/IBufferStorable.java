import java.io.IOException;

public interface IBufferStorable
{
	public void SaveOneLine(String filename) throws IOException;

	public void SaveSeparateLines(String filename) throws IOException;
}
