package calculator;

@SuppressWarnings("serial")
public class ParseValueException extends Exception {
	public ParseValueException() {
		super("Неверный формат строки");
	}
	public ParseValueException(String details) {
		super("Неверный формат строки. " + details);
	}
}
