package oop_usu.lesson14;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

public class FileTest16
{

    /**
     * @param args
     */
    public static void main(String [] args)
    {
        test3();
    }
    
    public static void test1()
    {
        String strUserHome = System.getProperty("user.home");
        System.out.println(strUserHome);
        File fUserHome = new File(strUserHome);
        System.out.println(fUserHome);
        File fSubDir = new File(fUserHome, "SubDir");
        System.out.println(fSubDir);
        File fSubDir1 = new File(strUserHome + "/SubDir");
        System.out.println(fSubDir1);
    }

    public static void test2()
    {
        File fUserHome = new File("C:/");
        System.out.println("Files of "+fUserHome);
        File [] files = fUserHome.listFiles();
        for (int iIdx = 0; iIdx < files.length; iIdx++)
        {
            File file = files[iIdx];
            String strLength = "";
            if (file.isDirectory())
            {  strLength = "<DIR>"; }
            else if (file.isFile())
            {  strLength = String.valueOf(file.length()); }
            else
            {  strLength = "unknown"; }
            String strMsg = file.getPath();
            while (strMsg.length() < 30)
            {
                strMsg = strMsg + " ";
            }
            strMsg = strMsg + strLength;
            System.out.println(strMsg);
        }
    }
    
    public static void dumpStream(InputStream is)
        throws IOException
    {
        int iValue;
        while ((iValue = is.read()) >= 0)
        {
            System.out.println(Integer.toHexString(iValue));
        }
    }
    
    public static void dumpStreamFast(InputStream is)
        throws IOException
    {
        byte [] buffer = new byte[1000];
        int iCount;
        while ((iCount = is.read(buffer)) >= 0)
        {
            for (int iIdx = 0; iIdx < iCount; iIdx++)
            {
                System.out.println(Integer.toHexString(buffer[iIdx]));
            }
        }
    }
    
    public static void test3()
    {
        File file = new File("input.txt");
        try
        {
            InputStream is = new FileInputStream(file);
            try
            {
                dumpStream(is);
            }
            finally
            {
                is.close();
            }
        }
        catch (IOException ex)
        { ex.printStackTrace(); }
        
    }
    
    public static void test4()
    {
        File file = new File("input.txt");
        try
        {
            InputStream is = new FileInputStream(file);
            try
            {
                BufferedInputStream bis = new BufferedInputStream(is);
                try
                {
                    dumpStreamFast(bis);
                }
                finally
                {
                    bis.close();
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

    public static void test4a()
    {
        File file = new File("input.txt");
        try
        {
            InputStream is = new FileInputStream(file);
            try
            {
                is = new BufferedInputStream(is);
                dumpStreamFast(is);
            }
            finally
            {
                is.close();
            }
        }
        catch (IOException ex)
        { ex.printStackTrace(); }
        
    }
}
