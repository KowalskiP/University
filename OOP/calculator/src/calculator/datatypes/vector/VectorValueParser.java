package calculator.datatypes.vector;

import calculator.AbstractValue;
import calculator.AbstractValueParser;
import calculator.ParseValueException;

public class VectorValueParser implements AbstractValueParser
{
    public AbstractValue parse(String value) throws ParseValueException {
        String values[];
        try
        {
            String value_stripped = value.substring(1, value.length() - 1);
            values = value_stripped.split(",");
        }
        catch(Exception e)
        {
            throw new ParseValueException();
        }

        if(values.length == 0)
            throw new ParseValueException("Не найдены координаты.");

        double iValues[] = new double[values.length];

        for(int i = 0; i < values.length; i++)
        {
            try
            {
                iValues[i] = Double.parseDouble(values[i]);
            }
            catch(Exception e)
            {
                throw new ParseValueException(e.getMessage());
            }
        }

        return new VectorValue(iValues);
    }

    public String getDatatypeName() {
        return "вектор";
    }
}
