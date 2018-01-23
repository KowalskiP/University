import java.io.*;
import java.net.*;
import java.util.*;


public class Page {

    private String pageUrl;
    private String contentCache = null;
    private HashMap<Character, ArrayList<Integer>> charCache =
            new HashMap<Character, ArrayList<Integer>>();

    public Page(String url)
    {
        pageUrl = url;
    }

    public char getCharAt(int idx) throws IOException
    {
        return getContent().charAt(idx);
    }

    public int findChar(char c) throws IOException {
        ArrayList<Integer> indexes = getIndexes(c);
        if(indexes.size() == 0)
            return -1;
        Random random = new Random();
        return indexes.get(random.nextInt(indexes.size()));
    }

    private synchronized ArrayList<Integer> getIndexes(char c) throws IOException
    {
        if(charCache.get(c) == null) {
            String content = getContent();
            ArrayList<Integer> listOfEntries = new ArrayList<Integer>();
            int lastPos = -1;
            while (true) {
                lastPos = content.indexOf(c, lastPos + 1);
                if (lastPos == -1)
                    break;
                listOfEntries.add(lastPos);
            }
            charCache.put(c, listOfEntries);
        }
        return charCache.get(c);
    }

    private synchronized String getContent() throws IOException
    {
        if(contentCache == null)
        {
            URL url = new URL(pageUrl);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    url.openConnection().getInputStream()));
            StringBuilder stringBuilder = new StringBuilder();
            char [] buffer = new char[4096];
            int len;
            while ((len = in.read(buffer)) != -1) {
                stringBuilder.append(buffer, 0, len);
            }
            contentCache = stringBuilder.toString();
        }
        return contentCache;
    }

}
