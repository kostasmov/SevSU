using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

public static class RleCompression
{
    public static byte[] Compress(Bitmap image)
    {
        List<byte> compressedData = new List<byte>();

        for (int y = 0; y < image.Height; y++)
        {
            byte currentPixel = image.GetPixel(0, y).R;
            int count = 1;

            for (int x = 1; x < image.Width; x++)
            {
                byte pixel = image.GetPixel(x, y).R;

                if (pixel == currentPixel && count < 255)
                {
                    count++;
                }
                else
                {
                    compressedData.Add((byte)count);
                    compressedData.Add(currentPixel);
                    currentPixel = pixel;
                    count = 1;
                }
            }

            compressedData.Add((byte)count);
            compressedData.Add(currentPixel);
        }

        return compressedData.ToArray();
    }

    public static Bitmap Decompress(byte[] compressedData, int width, int height)
    {
        Bitmap decompressedImage = new Bitmap(width, height);

        int dataIndex = 0;

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                byte count = compressedData[dataIndex++];
                byte pixel = compressedData[dataIndex++];
                for (int i = 0; i < count; i++)
                {
                    decompressedImage.SetPixel(x + i, y, Color.FromArgb(pixel, pixel, pixel));
                }

                x += count - 1;
            }
        }

        return decompressedImage;
    }

    public static void Main(string[] args)
    {
        Bitmap originalImage = new Bitmap("C:\\University\\image2.jpg");
        byte[] compressedData = Compress(originalImage);
        Bitmap decompressedImage = Decompress(compressedData, originalImage.Width, originalImage.Height);
        decompressedImage.Save("C:\\University\\decompressed2.jpg");
        Console.WriteLine("Сжатие и распаковка завершены.");
    }
}
