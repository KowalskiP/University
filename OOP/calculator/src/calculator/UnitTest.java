package calculator;
import calculator.datatypes.complex.ComplexValue;
import calculator.datatypes.complex.ComplexValueParser;
import calculator.datatypes.rational.RationalValue;
import calculator.datatypes.rational.RationalValueParser;
import calculator.datatypes.real.RealValueParser;
import calculator.datatypes.vector.VectorValue;
import calculator.datatypes.vector.VectorValueParser;
import calculator.datatypes.polynom.PolynomValue;
import calculator.datatypes.polynom.PolynomValueParser;

//import junit.framework.Assert;
import org.junit.*;

public class UnitTest
{
    @Test
    public void rationalParser() throws ParseValueException
    {
        RationalValueParser parser = new RationalValueParser();
        Assert.assertEquals(parser.parse("1/13"), new RationalValue(1, 13));
        Assert.assertEquals(parser.parse("1000/10"), new RationalValue(1000, 10));
        Assert.assertEquals(parser.parse("-14/7"), new RationalValue(-14, 7));
        Assert.assertEquals(parser.parse("13/14"), new RationalValue(13, 14));
        Assert.assertEquals(parser.parse("2/3"), new RationalValue(666, 999));
        Assert.assertEquals(parser.parse("0/4"), new RationalValue(0, 4));
    }


    @Test
    public void rationalArithmeticOperation() throws ParseValueException, DivisionByZeroException
    {
        RationalValue a = new RationalValue(3, 7);
        RationalValue b = new RationalValue(11, 13);
        Assert.assertEquals(a.add(b), new RationalValue(116, 91));
        Assert.assertEquals(a.sub(b), new RationalValue(-38, 91));
        Assert.assertEquals(a.mul(b), new RationalValue(33, 91));
        Assert.assertEquals(a.div(b), new RationalValue(39, 77));
    }

    @Test
    public void complexParser() throws ParseValueException
    {
        ComplexValueParser parser = new ComplexValueParser();
        Assert.assertEquals(parser.parse("1+1i"), new ComplexValue(1, 1));
        Assert.assertEquals(parser.parse("1-1i"),new ComplexValue(1, -1));
        Assert.assertEquals(parser.parse("-1+1i"), new ComplexValue(-1, 1));
        Assert.assertEquals(parser.parse("-1-1i"), new ComplexValue(-1, -1));
        Assert.assertEquals(parser.parse("-1.234+5.678i"), new ComplexValue(-1.234, 5.678));
    }

    @Test
    public void complexArithmeticOperation() throws ParseValueException, DivisionByZeroException
    {
        ComplexValue a = new ComplexValue(1, 1);
        ComplexValue b = new ComplexValue(-3, -4);
        Assert.assertEquals(a.add(b), new ComplexValue(-2, -3));
        Assert.assertEquals(a.sub(b), new ComplexValue(4, 5));
        Assert.assertEquals(a.mul(b), new ComplexValue(1, -7));
        Assert.assertEquals(a.div(b), new ComplexValue(-0.28, 0.04));
        a = new ComplexValue(4, 3);
        b = new ComplexValue(-2, 1.23);
        Assert.assertEquals(a.mul(b), new ComplexValue(-11.69, -1.08));
        //4+3i * -2+1.23i"
    }

    @Test
    public void vectorParser() throws ParseValueException
    {
        VectorValueParser parser = new VectorValueParser();
        Assert.assertEquals(parser.parse("(1,2,3)"), new VectorValue(new double[] {1, 2, 3}));
        Assert.assertEquals(parser.parse("(-1.123,+2,-3)"), new VectorValue(new double[] {-1.123, 2, -3}));
        Assert.assertEquals(parser.parse("(100,500)"), new VectorValue(new double[] {100,500}));
    }

    @Test
    public void vectorArithmeticOperation()
            throws ParseValueException, DivisionByZeroException, OperationNotSupportedException
    {
        VectorValueParser parser = new VectorValueParser();
        VectorValue a, b;

        a = new VectorValue(new double[] {1, 2, 3});
        b = new VectorValue(new double[] {3, 5, 6});

        Assert.assertEquals(a.add(b), new VectorValue(new double[] {4, 7, 9}));
        Assert.assertEquals(a.sub(b), new VectorValue(new double[] {-2, -3, -3}));

        a = new VectorValue(new double[] {1.23, 3.45});
        b = new VectorValue(new double[] {-3, 6});

        Assert.assertEquals(a.add(b), new VectorValue(new double[] {-1.77, 9.45}));
        Assert.assertEquals(a.sub(b), new VectorValue(new double[] {4.23, -2.55}));
    }

    @Test
    public void polynomialToString()
    {
        Assert.assertEquals(new PolynomValue(new double [] {-1, 2, 3}).toString(), "-1.0x^2+2.0x^1+3.0x^0");
        Assert.assertEquals(new PolynomValue(new double [] {1, 0, 0, 1}).toString(), "+1.0x^3+1.0x^0");
        Assert.assertEquals(new PolynomValue(new double [] {3, 0, 1, 0, -2}).toString(), "+3.0x^4+1.0x^2-2.0x^0");
    }

    @Test
    public void polynomialParser() throws ParseValueException
    {
        PolynomValueParser parser = new PolynomValueParser();
        Assert.assertEquals(parser.parse("+1x^4-2x^2+10x^0"), new PolynomValue(new double[] {1, 0, -2, 0, 10}));
        Assert.assertEquals(parser.parse("-10x^2"), new PolynomValue(new double[] {-10, 0, 0}));
        Assert.assertEquals(parser.parse("+1x^2-2x^1+1x^0"), new PolynomValue(new double[] {1, -2, 1}));
        Assert.assertEquals(
                parser.parse("+10x^5+3x^4-5x^3+1x^2-20x^1+50x^0"),
                new PolynomValue(new double[] {10, 3, -5, 1, -20, 50})
        );
        Assert.assertEquals(
                parser.parse("-13.5x^5-12.123x^4+32.009x^3+9.13x^2+6.17x^1-125.0001x^0"),
                new PolynomValue(new double[] {-13.5, -12.123, 32.009, 9.13, 6.17, -125.0001})
        );
    }

    @Test
    public void polynomialArithmeticOperation()
    {
        PolynomValue a = new PolynomValue(new double [] {1, 1});
        PolynomValue b = new PolynomValue(new double [] {1, -1});

        Assert.assertEquals(a.add(b), new PolynomValue(new double [] {2, 0}));
        Assert.assertEquals(a.sub(b), new PolynomValue(new double [] {0, 2}));
        Assert.assertEquals(a.mul(b), new PolynomValue(new double [] {1, 0, -1}));
        Assert.assertEquals(a.mul(a), new PolynomValue(new double [] {1, 2, 1}));
        Assert.assertEquals(b.mul(b), new PolynomValue(new double [] {1, -2, 1}));

        a = new PolynomValue(new double [] {10, 3, -5, 1, -20, 50});
        b = new PolynomValue(new double [] {-13, -12, 32, 9, 6, -125});

        Assert.assertEquals(
                a.mul(b),
                new PolynomValue(
                        new double [] {-130, -159, 349, 233, 175, 1655, 1636, 2051, 205, 2800, 6250}
                )
        );
    }

    @Test
    public void realCalculation()
            throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        Calculator calc = new Calculator(new RealValueParser());
        String expression;
        double answer;

        expression = "123.123 - 32.323 + 23.124 * 76.5 / 34.12 - 12.3232 * 32.1";
        answer = Double.parseDouble(calc.calculate(expression));
        Assert.assertEquals(answer, -252.928705932004689331770222743259085580304806565064, 1e-9);

        expression = "123.123 - ( 32.323 + 23.124 * 76.5 / 34.12 ) - 12.3232 * 32.1";
        answer = Double.parseDouble(calc.calculate(expression));
        Assert.assertEquals(answer, -356.620734067995310668229777256740914419695193434935, 1e-9);

        expression = "( 1 + 3 * ( 4 + 5 ) ) / ( 1 + 10 ) - 13 / 27 + 3 * ( 5 * 2 )";
        answer = Double.parseDouble(calc.calculate(expression));
        Assert.assertEquals(answer, 32.063973063973063973063973063973063973063973063973063, 1e-9);
    }

    @Test
    public void polynomialCalculation()
            throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        Calculator calc = new Calculator(new PolynomValueParser());
        PolynomValueParser parser = new PolynomValueParser();
        String expression;
        AbstractValue answer;

        //( x^4+3x^2+13 + 9x^3+7x ) * ( ( x^2 + 1 ) * ( x^2 + 1 ) )

        expression = "( +1x^4+3x^2+13x^0 + +9x^3+7x^1 ) * ( ( +1x^2 + +1x^0 ) * ( +1x^2 + +1x^0 ) )";
        answer = parser.parse(calc.calculate(expression));
        Assert.assertEquals(answer, new PolynomValue(new double [] {1, 9, 5, 25, 20, 23, 29, 7, 13}));

        // -4x^3-2x^2-x^1+13 * ( -2x^2+4x^1-5 + 5x^5-3x^2 )
        expression = "-4x^3-2x^2-1x^1+13x^0 * ( -2x^2+4x^1-5x^0 + +5x^5-3x^2 )";
        answer = parser.parse(calc.calculate(expression));
        Assert.assertEquals(answer, new PolynomValue(new double [] {-20, -10, -5, 85, -6, 17, -59, 57, -65}));
    }

    @Test
    public void complexCalculation()
            throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        Calculator calc = new Calculator(new ComplexValueParser());
        ComplexValueParser parser = new ComplexValueParser();
        String expression;

        expression = "( ( 4+3i * -2+1.23i - -0.5-10.01i / 2-3.2i + 3.13+1.45i ) *" +
                " 3.3-9i + -12+7.1i ) / ( 4.11-45.1i / ( 0.1-9i + 0.4+0.9i ) )";

        AbstractValue answer = parser.parse(calc.calculate(expression));
        Assert.assertEquals(answer, new ComplexValue(-4.877422625025742, 19.860210162686702));
    }

    @Test
    public void rationalCalculation()
            throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        Calculator calc = new Calculator(new RationalValueParser());
        RationalValueParser parser = new RationalValueParser();
        String expression;

        expression = "( 1/2 * ( 5/4 + 13/7 / 8/10 ) + 45/46 ) / ( 5/3 * 8/9 - ( 13/23 + 14/7 * ( 1/7 - 6/5 ) ) )";

        AbstractValue answer = parser.parse(calc.calculate(expression));
        Assert.assertEquals(answer, new RationalValue(60075, 65869));
    }

    @Test
    public void vectorCalculation()
            throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        Calculator calc = new Calculator(new VectorValueParser());
        VectorValueParser parser = new VectorValueParser();
        String expression;

        expression = "(+1.123,3.567) + (8.91,1.112) - (-13.14,15.16)";

        AbstractValue answer = parser.parse(calc.calculate(expression));
        Assert.assertEquals(answer, new VectorValue(new double [] {23.173, -10.481}));
    }

}
