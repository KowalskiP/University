import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.text.MessageFormat;
import java.util.Scanner;

public class FileTest17
{

    /**
     * @param args
     */
    public static void main(String [] args)
    {
        test5();
    }
    
    public static void test5()
    {
        File file = new File("data.bin");
        try
        {
            OutputStream os = new FileOutputStream(file);
            try
            {
                DataOutputStream dos = 
                    new DataOutputStream(new BufferedOutputStream(os));
                try
                {
                    dos.writeUTF("Here goes integer: ");
                    dos.writeInt(2007);
                    dos.flush();
                }
                finally
                {
                    dos.close();
                }
            }
            finally
            {
                os.close();
            }
            
            InputStream is = new FileInputStream(file);
            try
            {
                DataInputStream dis = new DataInputStream(new BufferedInputStream(is));
                try
                {
                    String strMsg = dis.readUTF() + dis.readInt();
                    System.out.println(strMsg);
                }
                finally
                {
                    dis.close();
                }
            }
            finally
            {
                is.close();
            }
        }
        catch (IOException ex)
        { ex.printStackTrace(); }
        
    }

    public static void test6()
    {
        try
        {
            String strTest = "�";
            byte [] data = strTest.getBytes("ISO8859-5");
            String strMsg = "";
            for (int iIdx = 0; iIdx < data.length; iIdx++)
            {
                int value = (data[iIdx] + 256) % 256;
                strMsg += Integer.toHexString(value);
                strMsg += " ";
            }
            System.out.println(strMsg);
            System.out.println(new String(data, "ISO8859-5"));
        }
        catch (UnsupportedEncodingException ex)
        {
            ex.printStackTrace();
        }
    }

    public static void test7()
    {
        File file = new File("output.txt");
        try
        {
            String strEncoding = System.getProperty("file.encoding");
            System.out.println("Input encoding is: "+strEncoding);
            
            System.out.print("Enter your name: ");
            Scanner scanner = new Scanner(new InputStreamReader(System.in, strEncoding));
            String strName = scanner.next();
            System.out.println("Hello, "+strName+"!");
            OutputStream os = new FileOutputStream(file);
            try
            {
                PrintWriter writer = new PrintWriter(
                   new OutputStreamWriter(new BufferedOutputStream(os), "Cp1251"));
                try
                {
                    writer.println("Hello, "+strName+"!");
                }
                finally
                {
                    writer.close();
                }
            }
            finally
            {
                os.close();
            }
        }
        catch (IOException ex)
        { ex.printStackTrace(); }
    }

    public static void test7a()
    {
        try
        {
            String strEncoding = System.getProperty("file.encoding");
            System.out.println("Input encoding is: "+strEncoding);
            
            System.out.print("Enter simple numeric expression: ");
            Scanner scanner = new Scanner(new InputStreamReader(System.in, strEncoding));
            scanner.useDelimiter("");
            String strVal1 = scanner.next("\\d+");
            String strOp = scanner.next("[\\+\\-\\*/]");
            String strVal2 = scanner.next("\\d+");
            
            PrintWriter writer = new PrintWriter(
               new OutputStreamWriter(new BufferedOutputStream(System.out), strEncoding));
            writer.println(
                MessageFormat.format("Parsed expression: {0} {1} {2}", new Object[]{strVal1, strOp, strVal2}));
            writer.flush();
        }
        catch (IOException ex)
        { ex.printStackTrace(); }
    }
}
