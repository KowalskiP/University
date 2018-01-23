import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

class RebusDecoder extends Thread
{
    private final PageManager pageManager;
    private final ArrayList<PageEntry> cipher;
    private final StringBuilder text;
    private final int from;
    private final int to;
    public volatile static int threadCounter = 0;
    RebusDecoder(PageManager mgr, ArrayList<PageEntry> in, StringBuilder out, int _from, int _to)
    {
        pageManager = mgr;
        cipher = in;
        text = out;
        from = _from;
        to = _to;
    }
    public void run()
    {
        StringBuilder slice = new StringBuilder();
        for(int i = from; i < to; i++)
        {
            slice.append(pageManager.getChar(cipher.get(i)));
        }
        text.replace(from, to, slice.toString());
        threadCounter--;
    }
}

class RebusEncoder extends Thread
{
    private final PageManager pageManager;
    private final PageEntry [] cipher;
    private final String text;
    private final int from;
    private final int to;
    public volatile static int threadCounter = 0;
    RebusEncoder(PageManager mgr, PageEntry [] in, String out, int _from, int _to)
    {
        pageManager = mgr;
        cipher = in;
        text = out;
        from = _from;
        to = _to;
    }
    public void run()
    {
        for(int i = from; i < to; i++)
        {
            cipher[i] = pageManager.findEntry(text.charAt(i));
        }
        threadCounter--;
    }
}

public class RebusParallels {
    private static final String usage =
            "java Rebus [decode|encode] [url_file_name] [input_file] [output_file]";
    private PageManager pageManager;

    public RebusParallels(String urlFileName) throws IOException
    {
        File file = new File(urlFileName);
        pageManager = new PageManager(file);
    }

    public ArrayList<Integer> encode(String str) throws IOException
    {
        PageEntry [] cipher = new PageEntry[str.length()];
        int size = 4096;
        for(int i = 0; i < str.length(); i += size) {
            RebusEncoder.threadCounter++;
            new RebusEncoder(pageManager, cipher, str, i, Math.min(i + size, str.length())).start();
        }
        while(RebusEncoder.threadCounter != 0)
        {
            try {
                Thread.sleep(100);
            } catch (InterruptedException ex) {}
        }
        ArrayList<Integer> result = new ArrayList<Integer>();
        for(PageEntry entry : cipher)
        {
            result.add((entry.charIdx << 8) | entry.pageId);
        }
        return result;
    }

    public String decode(ArrayList<Integer> list)
    {
        ArrayList<PageEntry> cipher = new ArrayList<PageEntry>();
        StringBuilder text = new StringBuilder();
        text.setLength(list.size());
        for(int val : list)
        {
            int pageId = val & 0xff;
            int charIdx = val >>> 8;
            cipher.add(new PageEntry(pageId, charIdx));
        }
        int size = 4096;
        for(int i = 0; i < list.size(); i += size) {
            RebusDecoder.threadCounter++;
            new RebusDecoder(pageManager, cipher, text, i, Math.min(i + size, list.size())).start();
        }
        while(RebusDecoder.threadCounter != 0)
        {
            try {
                Thread.sleep(100);
            } catch (InterruptedException ex) {}
        }
        return text.toString();
    }

    public static void main(String [] args) throws IOException
    {
        String mode;
        String urlFileName;
        String inputFileName;
        String outputFileName;
        try {
            mode = args[0];
            urlFileName = args[1];
            inputFileName = args[2];
            outputFileName = args[3];
        } catch (IndexOutOfBoundsException ex) {
            System.out.print(usage);
            return;
        }

        RebusParallels rebus = new RebusParallels(urlFileName);

        if(mode.equals("encode"))
        {
            BufferedReader reader = new BufferedReader(
                        new FileReader(inputFileName));
            StringBuilder stringBuilder = new StringBuilder();
            char [] buffer = new char[4096];
            int len;
            while ((len = reader.read(buffer)) != -1) {
                stringBuilder.append(buffer, 0, len);
            }
            ArrayList<Integer> cipher = rebus.encode(stringBuilder.toString());
            PrintWriter writer = new PrintWriter(new BufferedWriter(
                    new FileWriter(outputFileName)));
            for(int i : cipher) {
                writer.println(i);
            }
            reader.close();
            writer.close();
        }
        else if(mode.equals("decode"))
        {
            Scanner scanner = new Scanner(new File(inputFileName));
            ArrayList<Integer> cipher = new ArrayList<Integer>();
            while(scanner.hasNextInt())
            {
                cipher.add(scanner.nextInt());
            }
            String text = rebus.decode(cipher);
            BufferedWriter writer = new BufferedWriter(
                    new FileWriter(outputFileName));
            writer.write(text);
            scanner.close();
            writer.close();
        }
        else
        {
            System.out.println(usage);
        }
    }

}
