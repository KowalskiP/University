package calculator.datatypes.integer;

import calculator.AbstractValue;
import calculator.AbstractValueParser;
import calculator.ParseValueException;

public class IntegerValueParser implements AbstractValueParser {

	public AbstractValue parse(String value) throws ParseValueException {
		try {
			return new IntegerValue(Integer.parseInt(value));
		} catch (NumberFormatException exception) {
			throw new ParseValueException();
		}
	}

	public String getDatatypeName() {
		return "целые числа";
	}

}
