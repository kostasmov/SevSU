using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Text;

class JPEGCompression
{
    static void Main()
    {
        string inputFile = "C:/University/image.jpg";
        string compressedFile = "C:/University//result.jpg";

        Compress(inputFile, compressedFile);

        Console.WriteLine("Файл успешно сжат!");
    }

    static void Compress(string inputFile, string compressedFile)
    {
        using (Bitmap inputImage = new Bitmap(inputFile))
        {
            ImageCodecInfo jpegCodec = GetEncoderInfo(ImageFormat.Jpeg);

            EncoderParameters encoderParams = new EncoderParameters(1);
            encoderParams.Param[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Quality, 5L);

            inputImage.Save(compressedFile, jpegCodec, encoderParams);
        }
    }

    static ImageCodecInfo GetEncoderInfo(ImageFormat format)
    {
        ImageCodecInfo[] codecs = ImageCodecInfo.GetImageEncoders();
        foreach (ImageCodecInfo codec in codecs)
        {
            if (codec.FormatID == format.Guid)
            {
                return codec;
            }
        }
        return null;
    }
}
