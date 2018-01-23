/**
 * Created by amtig_000 on 19.09.2014.
 */
import java.util.Stack;

public class Message {
    String s;

    public Message(String str){
        s = str;
    }

    public int countWords(){
        int count = s.split(" ").length;
        return count;
    }

    public String reverse(){
        return new StringBuilder(s).reverse().toString();
    }

    public int count(char c){// возвращает кол-во вхождений символа в строку
        char[] array = s.toCharArray();
        int i = 0;
        int count_symbol = 0;
        while(i < array.length){
            if (array[i] == c) count_symbol++;
            i++;
        }
        return count_symbol;
    }

    public boolean isValid(){ // проверяет правильность расстановки скобок []{}()<> в строке
        char[] array = s.toCharArray();
        Stack stack = new Stack();
        int i = 0;
        while (i < array.length){
            if ((array[i]==')' | array[i]==']' | array[i]=='}' | array[i]=='>') & stack.isEmpty()) return false;
            if (array[i]=='(' | array[i]=='[' | array[i]=='{' | array[i]=='<'){
                stack.push(array[i]);
            }
            if (array[i]==')') if (stack.peek().toString().charAt(0) == '(') {
                stack.pop();
            } else return false;
            if (array[i]==']') if (stack.peek().toString().charAt(0) == '[') {
                stack.pop();
            } else return false;
            if (array[i]=='}') if (stack.peek().toString().charAt(0) == '{') {
                stack.pop();
            } else return false;
            if (array[i]=='>') if (stack.peek().toString().charAt(0) == '<') {
                stack.pop();
            } else return false;
            i++;
        }
        return stack.isEmpty();
    }

    public String encode(int shift){// увеличивает код каждого символа на shift
        int i = 0;
        char[] array = s.toCharArray();
        while (i<s.length()){
            char c = s.charAt(i);
            array[i] =(char)((int)c + shift);
            i++;
        }
        String str = new String(array);
        return str;
    }
}
