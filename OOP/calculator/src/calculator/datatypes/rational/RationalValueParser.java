package calculator.datatypes.rational;

import calculator.AbstractValue;
import calculator.AbstractValueParser;
import calculator.ParseValueException;

public class RationalValueParser implements AbstractValueParser
{
    public AbstractValue parse(String value) throws ParseValueException
    {
        String[] values = null;
        try
        {
             values = value.split("/");
        }
        catch (Exception e)
        {
            throw new ParseValueException();
        }

        if(values.length != 2)
            throw new ParseValueException();

        return new RationalValue(Integer.parseInt(values[0]), Integer.parseInt(values[1]));
    }


    public String getDatatypeName()
    {
        return "рациональные числа";
    }

}
