import java.util.*;
import java.io.*;

class PageManagerException extends RuntimeException
{
    PageManagerException(String msg)
    {
        super(msg);
    }
}

public class PageManager {
    private ArrayList<Page> pageList = new ArrayList<Page>();

    public PageManager(File inputFile) throws IOException
    {
        BufferedReader reader = new BufferedReader(
                new FileReader(inputFile)
        );
        while(reader.ready())
        {
            addPage(new Page(reader.readLine()));
        }
    }

    public void addPage(Page page)
    {
        pageList.add(page);
    }

    public char getChar(PageEntry entry) throws PageManagerException
    {
        Page page = pageList.get(entry.pageId);
        try {
            return page.getCharAt(entry.charIdx);
        } catch (IOException ex) {
            ex.printStackTrace();
            throw new PageManagerException(String.format(
                    "Не удалось получить букву %d на странице %d",
                    entry.charIdx, entry.pageId));
        }
    }

    public PageEntry findEntry(char c) throws PageManagerException
    {
        ArrayList<Integer> indexs = new ArrayList<Integer>();
        for(int i = 0; i < pageList.size(); i++)
            indexs.add(i);
        Collections.shuffle(indexs);
        try {
            for (int pageId : indexs) {
                int charIdx = pageList.get(pageId).findChar(c);
                if (charIdx != -1)
                    return new PageEntry(pageId, charIdx);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
            throw new PageManagerException(
                    String.format("Не удалось найти букву %c", c));
        }
        throw new PageManagerException(
                String.format("Не удалось найти букву %c", c));
    }
}
