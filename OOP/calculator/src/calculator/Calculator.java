package calculator;

import java.util.*;


public class Calculator {
	private final AbstractValueParser valueParser;
    private Stack<String> operatorsStack = new Stack<String>();
    private Stack<AbstractValue> argsStack = new Stack<AbstractValue>();

	public Calculator(AbstractValueParser valueParser) {
		this.valueParser = valueParser;
	}

	public String calculate(String expression)
			throws DivisionByZeroException, SyntaxErrorException, ParseValueException, OperationNotSupportedException
    {
        operatorsStack.clear();
        argsStack.clear();
        String [] operands = expression.split(" ");
		return calculate(operands).toString();
	}

    private int getOperatorPriority(String operator)
    {
        if(operator.equals("("))
            return 0;
        if(operator.equals("+") || operator.equals("-"))
            return 1;
        if(operator.equals("*") || operator.equals("/"))
            return 2;
        return -1;
    }

    private boolean isOperator(String testingStr)
    {
        return testingStr.equals("+") ||
                testingStr.equals("-") ||
                testingStr.equals("*") ||
                testingStr.equals("/") ||
                testingStr.equals("(");
    }

    private void makeCalculation()
            throws OperationNotSupportedException, DivisionByZeroException, SyntaxErrorException
    {
        AbstractValue left, right, result;
        String operator;
        try
        {
            right = argsStack.pop();
            left = argsStack.pop();
            operator = operatorsStack.pop();
        }
        catch(EmptyStackException e)
        {
            throw new SyntaxErrorException();
        }

        if(operator.equals("+"))
        {
            result = left.add(right);
        }
        else if(operator.equals("-"))
        {
            result = left.sub(right);
        }
        else if(operator.equals("*"))
        {
            result = left.mul(right);
        }
        else if(operator.equals("/"))
        {
            result = left.div(right);
        }
        else
        {
            throw new SyntaxErrorException();
        }
        argsStack.push(result);
    }

	private AbstractValue calculate(String [] operands)
            throws DivisionByZeroException, OperationNotSupportedException, SyntaxErrorException, ParseValueException
    {

        for (int i = 0; i < operands.length; i++)
        {
            if(operands[i].equals(")"))
            {
                while(!operatorsStack.peek().equals("("))
                {
                    makeCalculation();
                }
                operatorsStack.pop();
            }
            else if(operands[i].equals("("))
            {
                operatorsStack.push(operands[i]);
            }
            else if(isOperator(operands[i]))
            {
                while(!operatorsStack.empty() &&
                        getOperatorPriority(operatorsStack.peek()) >= getOperatorPriority(operands[i]))
                {
                    makeCalculation();
                }
                operatorsStack.push(operands[i]);
            }
            else
            {
                argsStack.push(valueParser.parse(operands[i]));
            }
        }

        while(!operatorsStack.empty())
        {
            makeCalculation();
        }

        if(argsStack.size() == 1)
        {
            return argsStack.pop();
        }
        else
        {
            throw new SyntaxErrorException();
        }
	}
}
