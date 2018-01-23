package calculator.datatypes.polynom;

import calculator.AbstractValue;
import calculator.OperationNotSupportedException;

public class PolynomValue extends AbstractValue
{
    double [] coefficients;

    public PolynomValue(double[] coefficients)
    {
        this.coefficients = coefficients.clone();
    }

    public AbstractValue add(AbstractValue operand)
    {
        int firstSize = coefficients.length;
        int secondSize = ((PolynomValue)operand).coefficients.length;
        int resultSize = Math.max(firstSize, secondSize);

        double [] resultCoefficient = new double[resultSize];

        for(int i = 0; i < firstSize; i++)
        {
            resultCoefficient[resultSize - 1 - i] = coefficients[firstSize - 1 - i];
        }

        for(int i = 0; i < secondSize; i++)
        {
            resultCoefficient[resultSize - 1 - i] += ((PolynomValue)operand).coefficients[secondSize - 1 - i];
        }

        return new PolynomValue(resultCoefficient);
    }

    public AbstractValue sub(AbstractValue operand)
    {
        double [] secondCoefficients = ((PolynomValue)operand).coefficients.clone();
        for(int i = 0; i < secondCoefficients.length; i++)
        {
            secondCoefficients[i] *= -1;
        }

        return add(new PolynomValue(secondCoefficients));
    }

    public AbstractValue mul(AbstractValue operand)
    {
        int firstSize = coefficients.length;
        int secondSize = ((PolynomValue)operand).coefficients.length;
        int resultSize = firstSize + secondSize - 1;
        double [] resultCoefficients = new double [resultSize];
        double [] otherCoefficients = ((PolynomValue)operand).coefficients;

        for(int i = 0; i < firstSize; i++)
        {
            for(int j = 0; j < secondSize; j++)
            {
                int firstExp = firstSize - 1 - i;
                int secondExp = secondSize - 1 - j;
                resultCoefficients[resultSize - 1 - (firstExp + secondExp)] += coefficients[i] * otherCoefficients[j];
            }
        }

        return new PolynomValue(resultCoefficients);
    }

    public AbstractValue div(AbstractValue operand) throws OperationNotSupportedException
    {
        double [] dividend = coefficients.clone();
        double [] divisor = ((PolynomValue) operand).coefficients.clone();
        double [] remainder = coefficients.clone();
        double [] quotient = new double[remainder.length - divisor.length +1];

        for (int i=0; i<quotient.length; i++){
            double coeff = remainder[remainder.length - i -1]/divisor[divisor.length];
            quotient[quotient.length - i - 1] = coeff;
            for (int j = 0; j < divisor.length; j++)
            {
                remainder[remainder.length - i - j - 1] -= coeff * divisor[divisor.length - j - 1];
            }
        }

        return new PolynomValue(quotient);
    }

    public String toString()
    {
        StringBuilder result = new StringBuilder();
        double eps = 1e-9;

        for(int i = 0; i < coefficients.length; i++)
        {
            if (Math.abs(coefficients[i]) < eps)
            {
                continue;
            }

            if (coefficients[i] > 0)
            {
                result.append("+");
            }

            result.append(coefficients[i]);
            result.append("x^");
            result.append(coefficients.length - 1 - i);
        }
        String resStr = result.toString();
        return resStr.equals("") ? "0x^0" : resStr;
    }

    public boolean equals(Object operand)
    {
        double eps = 1e-9;
        if(operand instanceof PolynomValue)
        {
            double [] operandCoefficients = ((PolynomValue)operand).coefficients;
            if(coefficients.length != operandCoefficients.length)
            {
                return false;
            }
            for(int i = 0; i < coefficients.length; i++)
            {
                double x = coefficients[i];
                double y = operandCoefficients[i];
                if(Math.abs(x - y) >= eps)
                {
                    return false;
                }
                return true;
            }
        }
        return false;
    }

    public int hashCode()
    {
        int hash = 0;
        for(int i = 0; i < coefficients.length; i++)
        {
            hash += (int)coefficients[i];
        }
        return hash;
    }
}
