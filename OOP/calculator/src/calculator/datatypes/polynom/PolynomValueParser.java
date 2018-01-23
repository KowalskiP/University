package calculator.datatypes.polynom;

import calculator.AbstractValueParser;
import calculator.AbstractValue;
import calculator.ParseValueException;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PolynomValueParser implements AbstractValueParser
{
    private final Pattern polynomialRegexp =
            Pattern.compile("^((?:\\+|-)\\d+(?:\\.\\d+)?x\\^\\d+)+$");
    private final Pattern monomialRegexp =
            Pattern.compile("((?:\\+|-)\\d+(?:\\.\\d+)?)x\\^(\\d+)");
    private Matcher matcher;

    public AbstractValue parse(String value) throws ParseValueException
    {
        matcher = polynomialRegexp.matcher(value);
        if(!matcher.find())
            throw new ParseValueException(value);

        matcher = monomialRegexp.matcher(value);
        ArrayList<Integer> exp = new ArrayList<Integer>();
        ArrayList<Double> coefficient = new ArrayList<Double>();

        int maxExp = 0;

        int monomialCounter = 0;

        while(matcher.find())
        {
            double currentCoefficient = Double.parseDouble(matcher.group(1));
            coefficient.add(currentCoefficient);

            int currentExp = Integer.parseInt(matcher.group(2));
            exp.add(currentExp);

            maxExp = Math.max(maxExp, currentExp);
            monomialCounter++;
        }

        double [] coefficients = new double [maxExp + 1];

        for(int i = 0; i < monomialCounter; i++)
        {
            coefficients[maxExp - exp.get(i)] += coefficient.get(i);
        }

        return new PolynomValue(coefficients);
    }


    public String getDatatypeName()
    {
        return "многочлены";
    }
}
