package calculator.datatypes.vector;
import calculator.AbstractValue;
import calculator.OperationNotSupportedException;

public class VectorValue extends AbstractValue
{
    private double values[];

    public VectorValue(double [] values)
    {
        this.values = values.clone();
    }

    public AbstractValue mul(AbstractValue operand) throws OperationNotSupportedException
    {
        throw new OperationNotSupportedException("*");
    }

    public AbstractValue div(AbstractValue operand) throws OperationNotSupportedException
    {
        throw new OperationNotSupportedException("/");
    }

    public AbstractValue add(AbstractValue operand) throws OperationNotSupportedException
    {
        VectorValue op = (VectorValue)operand;
        if(op.values.length != values.length)
            throw new OperationNotSupportedException("\"сложение векторов разной длины\"");

        double result_values[] = values.clone();
        for(int i = 0; i < values.length; i++)
        {
            result_values[i] += op.values[i];
        }
        return new VectorValue(result_values);
    }

    public AbstractValue sub(AbstractValue operand) throws OperationNotSupportedException
    {
        VectorValue op = (VectorValue)operand;
        if(op.values.length != values.length)
            throw new OperationNotSupportedException("\"вычитание векторов разной длины\"");

        double result_values[] = values.clone();
        for(int i = 0; i < values.length; i++)
        {
            result_values[i] -= op.values[i];
        }
        return new VectorValue(result_values);
    }

    public String toString()
    {
        StringBuilder result = new StringBuilder(100);
        result.append("(");
        result.append(values[0]);
        for(int i = 1; i < values.length; i++)
        {
            result.append(",");
            result.append(values[i]);
        }
        result.append(")");
        return result.toString();
    }

    public boolean equals(Object operand)
    {
        if(operand instanceof VectorValue)
        {
            VectorValue vectorOperand = (VectorValue)operand;
            if(values.length != vectorOperand.values.length)
                return false;

            double eps = 1e-9;
            for(int i = 0; i < values.length; i++)
            {
                if(Math.abs(values[i] - vectorOperand.values[i]) >= eps)
                {
                    return false;
                }
            }

            return true;
        }
        return false;
    }

    public int hashCode()
    {
        int hash = 0;
        for(double coordinate : values)
        {
            hash += (int)coordinate;
        }
        return hash;
    }
}
