import java.io.*;
import java.util.Arrays;

public class CodeAnalyze {
    private final static String testFile = "dialog/idiot.txt";
    private final static String Sigma = "абвгдеёжзийкламнопрстуфхцчшщъыьэюя";
    private final static String [] ENCODINGS = new String [] {
            "cp866",
            "cp1251",
            "koi8-r",
            "iso-8859-5",
            "utf-8",
            "utf-16le",
            "utf-16be",
    };

    private double [] Frequency;

    private double [] getFrequency(char[] text)
    {
        double [] frequencyVector = new double [Sigma.length()];
        int sum = 0;
        for(char ch : text)
        {
            int idx = Sigma.indexOf(Character.toLowerCase(ch));
            if(idx != -1)
            {
                sum++;
                frequencyVector[idx]++;
            }
        }
        for(int i = 0; i < Sigma.length(); i++)
        {
            frequencyVector[i] /= sum;
        }
        return frequencyVector;
    }

    private double getDistance(double[] first, double[] second)
    {
        double result = 0;
        for(int i = 0; i < Sigma.length(); i++)
        {
            double value = first[i] - second[i];
            result += value * value;
        }
        return Math.sqrt(result);
    }

    private char [] encodeData(byte [] data) throws
            IOException
    {

        double minDist = Double.MAX_VALUE;
        String minEncoding = "";
        byte [] buff = new byte [data.length];
        for(int i = 0, j = 0; i < data.length; i++)
        {
            if(data[i] != '\n')
            {
                buff[j++] = data[i];
            }
        }
        for(String encoding : ENCODINGS)
        {
            String text = new String(buff, encoding);
            double [] frequencyVector = getFrequency(text.toCharArray());
            double distance = getDistance(frequencyVector, Frequency);
            if(distance < minDist)
            {
                minDist = distance;
                minEncoding = encoding;
            }
            System.out.println(encoding);
            System.out.println(Frequency);
            System.out.println(frequencyVector);
        }

        System.out.println(minEncoding);

        StringBuilder result = new StringBuilder();
        for(int i = 0, j = 0; i < data.length; i++)
        {
            if(data[i] != '\n' || i + 1 == data.length)
            {
                buff[j++] = data[i];
            }
            else
            {
                result.append(new String(Arrays.copyOf(buff, j), minEncoding));
                result.append('\n');
                j = 0;
            }
        }

        return result.toString().toCharArray();
    }

    private char [] mergeD(char[] first, char[] second)
    {
        char [] result = new char[first.length + second.length];
        int i = 0, j = 0, k = 0;
        while(i < first.length || j < second.length)
        {
            if(k == 0 && i < first.length)
            {
                result[i + j] = first[i];
                if(first[i] == '\n')
                    k = 1;
                i++;
            }
            else if(j < second.length)
            {
                result[i + j] = second[j];
                if(second[j] == '\n')
                    k = 0;
                j++;
            }
            else
            {
                k = 1 - k;
            }
        }
        return result;
    }

    private char [] cutZeros(char [] text)
    {
        int idx = 0;
        for(; idx < text.length; idx++)
        {
            if(text[idx] == 0)
                break;
        }
        return Arrays.copyOf(text, idx);
    }

    public void encode(String inputFileName, String outputFileName) throws
            IOException
    {
        File inputFile = new File(inputFileName);
        int fileLength = (int)inputFile.length();
        byte [] data = new byte [fileLength];
        byte [][] dialogs = new byte [][] {
                new byte [fileLength],
                new byte [fileLength],
        };
        int [] dialogsSizes = new int [] {0, 0};
        FileInputStream fileInputStream = new FileInputStream(inputFile);
        fileInputStream.read(data);
        fileInputStream.close();
        int dialogIdx = 0;
        for(byte b : data)
        {
            int currentDialogSize = dialogsSizes[dialogIdx];
            dialogs[dialogIdx][currentDialogSize] = b;
            dialogsSizes[dialogIdx]++;
            if(b == '\n')
                dialogIdx = 1 - dialogIdx;
        }

        char [] encodedData = cutZeros(mergeD(encodeData(dialogs[0]), encodeData(dialogs[1])));
        FileOutputStream fos = new FileOutputStream(outputFileName);
//        Writer out = new OutputStreamWriter(fos, "utf8");
//        out.write(encodedData);
//        out.close();
        FileWriter writer = new FileWriter(outputFileName);
        writer.write(encodedData);
        writer.close();
    }

    public CodeAnalyze(String fileName) throws
            IOException
    {
        FileReader reader = new FileReader(fileName);
        StringBuilder text = new StringBuilder();
        while(reader.ready())
        {
            char ch = (char)reader.read();
            text.append(ch);
        }
        reader.close();

        Frequency = getFrequency(text.toString().toCharArray());
    }

    public static void main(String [] args) throws Exception
    {
        CodeAnalyze analyzer = new CodeAnalyze(testFile);

        String inputFileName;
        String outputFileName;

        try {
            inputFileName = args[0];
            outputFileName = args[1];
        } catch(ArrayIndexOutOfBoundsException ex) {
            System.out.println("java CodeAnalyze [input_file_name] [output_file_name]");
            return;
        }

        analyzer.encode(inputFileName, outputFileName);
    }
}