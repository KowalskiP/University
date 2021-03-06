/**
 * Created by Антон on 17.02.2015.
 */

import java.io.*;


public class Main {
    public static void main(String [] args) {
        String s = readInput("output.txt", "UTF8");
        System.out.println(s);
        writeOutput(s,"outputUTF8.txt", "Cp1251");
    }
    public static String readInput (String fn, String enc) {
            File file = new File(fn);
            StringBuffer buffer = new StringBuffer();
            try
            {
                FileInputStream fis = new FileInputStream(file);
                InputStreamReader isr = new InputStreamReader(fis, enc);
                Reader in = new BufferedReader(isr);
                int ch;
                while ((ch = in.read()) > -1) {
                    buffer.append((char) ch);
                }
                in.close();
                return buffer.toString();

            }
            catch (IOException ex)
            {
                ex.printStackTrace();
                return null;
            }
    }

    public static void writeOutput(String str, String fn, String enc)
    {
        try {
            FileOutputStream fos = new FileOutputStream(fn);
            Writer out = new OutputStreamWriter(fos, enc);
            out.write(str);
            out.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }

    }
}
