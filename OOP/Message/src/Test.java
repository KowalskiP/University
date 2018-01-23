/**
 * Created by amtig_000 on 19.09.2014.
 */
public class Test {
    public static void test(String got, String expected){
        String prefix;
        if (got.equals(expected)) prefix = " OK ";
        else prefix = " X ";
        System.out.printf("%s got: %s expected: %s", prefix, got, expected);
        System.out.println();
    }
    public static void test(int got, int expected){
        String prefix;
        if (got == expected) prefix = " OK ";
        else prefix = " X ";
        System.out.printf("%s got: %d expected: %d", prefix, got, expected);
        System.out.println();
    }
    public static void test(boolean got, boolean expected){
        String prefix;
        if (got == expected) prefix = " OK ";
        else prefix = " X ";
        System.out.printf("%s got: %s expected: %s", prefix, got, expected);
        System.out.println();
    }
    public static void main(String [] args){
        Message test_message_1=new Message("abrakadabra");
        Message test_message_2=new Message(") [ 2 + ( { 4 ) - 5 } ] + 2");
        Message test_message_3=new Message("a roza upala na lapu azora");

        test(test_message_1.countWords(), 1);
        test(test_message_2.countWords(), 11);
        test(test_message_3.countWords(), 6);

        test(test_message_1.reverse(), "arbadakarba");
        test(test_message_2.reverse(), "2 + ] } 5 - 4 { + 2 [");
        test(test_message_3.reverse(), "aroza upal an alapu azor a");

        test(test_message_1.count('a'), 5);
        test(test_message_2.count('2'), 2);
        test(test_message_3.count('a'), 8);

        test(test_message_2.isValid(), false);

        test(test_message_1.encode(9), "jk{jtjmjk{j");
        test(test_message_3.encode(4), "e$vs~e$ytepe$re$pety$e~sve");
    }
}
