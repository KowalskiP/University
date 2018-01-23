package calculator;

public abstract class AbstractValue {
	public abstract AbstractValue add(AbstractValue operand)
			throws OperationNotSupportedException;

	public abstract AbstractValue sub(AbstractValue operand)
			throws OperationNotSupportedException;

	public abstract AbstractValue mul(AbstractValue operand)
			throws OperationNotSupportedException;

	public abstract AbstractValue div(AbstractValue operand)
			throws DivisionByZeroException, OperationNotSupportedException;

	public abstract String toString();
}
