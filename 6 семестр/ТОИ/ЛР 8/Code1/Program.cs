using System;
using System.Collections.Generic;
using System.Linq;

public class TagCloudBuilder
{
    public Dictionary<string, int> BuildTagCloud(string text)
    {
        Dictionary<string, int> tagCloud = new Dictionary<string, int>();
        string[] words = text.Split(new[] { ' ', ',', '.', ';', ':', '!', '?' }, StringSplitOptions.RemoveEmptyEntries);

        foreach (string word in words)
        {
            if (IsNounInNominativeCase(word) || word.Length >= 3)
            {
                string normalizedWord = word.ToLower();

                if (tagCloud.ContainsKey(normalizedWord))
                {
                    tagCloud[normalizedWord]++;
                }
                else
                {
                    tagCloud.Add(normalizedWord, 1);
                }
            }
        }

        return tagCloud;
    }

    private bool IsNounInNominativeCase(string word)
    {
        return false;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        string text = "Солнце светит над городом, где дети играют в парке.";
        TagCloudBuilder tagCloudBuilder = new TagCloudBuilder();
        Dictionary<string, int> tagCloud = tagCloudBuilder.BuildTagCloud(text);

        foreach (KeyValuePair<string, int> tag in tagCloud)
        {
            Console.WriteLine($"Слово: {tag.Key}, Количество: {tag.Value}");
        }
    }
}
