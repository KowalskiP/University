/**
 * Created by Антон on 29.03.2015.
 */
import java.io.*;
import java.util.*;
import java.text.*;

public class Sandbox {

    static synchronized int f(int n){
        if (n == 1) return 1;
        return f(n-1) * n;
    }

    public static void main(String args[]) throws IOException {
//        Reader r = new StringReader("abcdefghijklmnopqrstuvwxyz");
//        BufferedReader br1 = new BufferedReader(r);
//        BufferedReader br2 = new BufferedReader(r);
//        int c1 = br1.read(); // ?
//        int c2 = br2.read(); // ?
//        System.out.println(c1);
//        System.out.println(c2);
//        c1 = br1.read(); // ?
//        c2 = br2.read(); // ?
//        System.out.println(c1);
//        System.out.println(c2);
//        System.out.println(f(5));
        Test.main(new String[5]);
    }
}

class MyComparator implements Comparator
{
    public int compare(Object val1, Object val2)
    {
        int i1 = ((String)val1).length();
        int i2 = ((String)val2).length();
        return (i1 < i2) ? -1 : (i1 > i2) ? 1 :
                ((Comparable)val1).compareTo(val2);
    }
}
class Test
{
    public static void print(String [] arr)
    {
        for (String val : arr)
        {
            System.out.print(val); System.out.print(" ");
        }
        System.out.println();
    }
    public static void main(String [] args)
    {
        String [] values = new String[]
                {"one", "two", "three", "four",
                        "ONE", "TWO", "THREE", "FOUR"};
        String [] sorted1 = values.clone();
        String [] sorted2 = values.clone();
        Locale locale = new Locale("ru", "RU");
        Collator collator = Collator.getInstance(locale);
        Arrays.sort(sorted1);
        Arrays.sort(sorted2, collator);
        print(sorted1);
        print(sorted2);
    }
}
