package calculator.datatypes.complex;

import calculator.AbstractValueParser;
import calculator.AbstractValue;
import calculator.ParseValueException;

import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class ComplexValueParser implements AbstractValueParser
{
    private final Pattern complexRegexp = Pattern.compile("^((?:\\+|-)?\\d+(?:\\.\\d+)?)((?:\\+|-)\\d+(?:\\.\\d+)?)i$");
    private Matcher matcher;

    public AbstractValue parse(String value) throws ParseValueException
    {

        try
        {
            matcher = complexRegexp.matcher(value);
            boolean found = matcher.find();
            if(!found)
                throw new ParseValueException(value + " не соответствует шаблону");
        }
        catch(Exception e)
        {
            throw new ParseValueException(e.getMessage());
        }

        double re = Double.parseDouble(matcher.group(1));
        double im = Double.parseDouble(matcher.group(2));
        return new ComplexValue(re, im);
    }


    public String getDatatypeName()
    {
        return "комплексные числа";
    }

}
