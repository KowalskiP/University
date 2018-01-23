package calculator.datatypes.rational;

import calculator.AbstractValue;
import calculator.DivisionByZeroException;

public class RationalValue extends AbstractValue
{
    private final int p, q;

    private static int gcd(int a, int b)
    {
        return b == 0 ? a : gcd(b, a % b);
    }

    public RationalValue(int p, int q)
    {
        this.p = p / gcd(Math.abs(p), q);
        this.q = q / gcd(Math.abs(p), q);
    }

    public AbstractValue add(AbstractValue operand)
    {
        return new RationalValue(p * ((RationalValue)operand).q + q * ((RationalValue)operand).p,
                q * ((RationalValue)operand).q);
    }

    public AbstractValue sub(AbstractValue operand)
    {
        return new RationalValue(p * ((RationalValue)operand).q - q * ((RationalValue)operand).p,
                q * ((RationalValue)operand).q);
    }

    public AbstractValue mul(AbstractValue operand)
    {
        return new RationalValue(p * ((RationalValue)operand).p, q * ((RationalValue)operand).q);
    }

    public AbstractValue div(AbstractValue operand) throws DivisionByZeroException
    {
        if(((RationalValue)operand).p == 0)
            throw new DivisionByZeroException();
        return new RationalValue(p * ((RationalValue)operand).q, q * ((RationalValue)operand).p);
    }

    public String toString()
    {
        return p + "/" + q;
    }

    public boolean equals(Object operand)
    {
        if(operand instanceof RationalValue)
        {
            int other_p = ((RationalValue)operand).p;
            int other_q = ((RationalValue)operand).q;
            return p == other_p && q == other_q;
        }
        return false;
    }

    public int hashCode()
    {
        return p + q;
    }

}
