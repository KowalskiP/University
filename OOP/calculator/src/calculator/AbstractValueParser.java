package calculator;

public interface AbstractValueParser {
	AbstractValue parse(String value) throws ParseValueException;
	String getDatatypeName();
}
