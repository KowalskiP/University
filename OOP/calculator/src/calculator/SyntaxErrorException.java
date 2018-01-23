package calculator;

@SuppressWarnings("serial")
public class SyntaxErrorException extends Exception {
    public SyntaxErrorException() {
        super("Ошибка синтаксиса");
    }
}
