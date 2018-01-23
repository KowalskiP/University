package calculator.datatypes.integer;

import calculator.AbstractValue;
import calculator.DivisionByZeroException;

public class IntegerValue extends AbstractValue {
	private final int value;

	public IntegerValue(int value) {
		super();
		this.value = value;
	}

	public String toString() {
		return Integer.toString(value);
	}

	public AbstractValue add(AbstractValue operand) {
		return new IntegerValue(value + ((IntegerValue) operand).value);
	}

	public AbstractValue sub(AbstractValue operand) {
		return new IntegerValue(value - ((IntegerValue) operand).value);
	}

	public AbstractValue mul(AbstractValue operand) {
		return new IntegerValue(value * ((IntegerValue) operand).value);
	}

	public AbstractValue div(AbstractValue operand)
			throws DivisionByZeroException {
		int intValue = ((IntegerValue) operand).value;
		if (intValue == 0)
			throw new DivisionByZeroException();
		return new IntegerValue(value / intValue);
	}

}
