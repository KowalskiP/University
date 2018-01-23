package calculator.datatypes.complex;

import calculator.AbstractValue;
import calculator.DivisionByZeroException;

public class ComplexValue extends AbstractValue
{
    private final double real, imaginary;

    public ComplexValue(double re, double im) {
        real = re;
        imaginary = im;
    }

    public String toString() {
        char sign = imaginary >= 0 ? '+' : '-';
        return Double.toString(real) + sign + Double.toString(Math.abs(imaginary)) + "i";
    }

    public AbstractValue add(AbstractValue operand)
    {
        return new ComplexValue(
                real + ((ComplexValue)operand).real,
                imaginary + ((ComplexValue)operand).imaginary
        );
    }

    public AbstractValue sub(AbstractValue operand) {
        return new ComplexValue(
                real - ((ComplexValue)operand).real,
                imaginary - ((ComplexValue)operand).imaginary
        );
    }

    public AbstractValue mul(AbstractValue operand) {
        double a = real;
        double b = imaginary;
        double c = ((ComplexValue)operand).real;
        double d = ((ComplexValue)operand).imaginary;
        double re = (a * c - b * d);
        double im = (a * d + b * c);
        return new ComplexValue(re, im);

    }

    public AbstractValue div(AbstractValue operand) throws DivisionByZeroException {
        double a = real;
        double b = imaginary;
        double c = ((ComplexValue)operand).real;
        double d = ((ComplexValue)operand).imaginary;
        double q = c * c + d * d;
        if(Double.compare(d, 0) == 0)
        {
            throw new DivisionByZeroException();
        }
        double re = (a * c + b * d) / q;
        double im = (b * c - a * d) / q;
        return new ComplexValue(re, im);
    }

    public boolean equals(Object operand)
    {
        if(operand instanceof ComplexValue)
        {
            double eps = 1e-9;
            double other_real = ((ComplexValue)operand).real;
            double other_imaginary = ((ComplexValue)operand).imaginary;
            return Math.abs(real - other_real) < eps && Math.abs(imaginary - other_imaginary) < eps;
        }
        return false;
    }

    public int hashCode()
    {
        return (int)(real + imaginary);
    }

}
