package calculator.console;

import java.util.Scanner;

import calculator.AbstractValueParser;
import calculator.Calculator;
import calculator.datatypes.complex.ComplexValueParser;
import calculator.datatypes.integer.IntegerValueParser;
import calculator.datatypes.rational.RationalValueParser;
import calculator.datatypes.real.RealValueParser;
import calculator.datatypes.vector.VectorValueParser;
import calculator.datatypes.polynom.PolynomValueParser;

public class Program {

	private final Scanner scanner;

	private final Calculator calc;

	private AbstractValueParser[] valueParsers;

	public Program() {
		scanner = new Scanner(System.in);
		valueParsers = new AbstractValueParser[] {
                new IntegerValueParser(),
				new RealValueParser(),
                new RationalValueParser(),
                new ComplexValueParser(),
                new VectorValueParser(),
                new PolynomValueParser()
        };
		AbstractValueParser parser = inputValueParser();
		System.out.println("Работаем с типом '" + parser.getDatatypeName()
				+ "'");
		calc = new Calculator(parser);
	}

	private AbstractValueParser inputValueParser() {
		showChoises();
		int choise = Integer.parseInt(scanner.nextLine());
		if (choise >= 1 && choise <= valueParsers.length)
			return valueParsers[choise - 1];
		else {
			System.out.println("Неверный выбор!");
			return inputValueParser();
		}
	}

	private void showChoises() {
		System.out.println("Вам нужно выбрать тип данных. Возможные варианты:");
		for (int i = 0; i < valueParsers.length; i++)
			System.out.println("  " + (i + 1) + ". "
					+ valueParsers[i].getDatatypeName());
	}

	public static void main(String args[]) {
		try {
			Program instance = new Program();
			instance.run(args);
		} catch (Exception e) {
			e.printStackTrace(System.out);
		}
	}

	private void run(String[] args) {
		while (true) {
			String expression = scanner.nextLine();
			if (expression.equals("exit"))
				break;
			try {
				System.out.println(" = " + calc.calculate(expression));
			} catch (Exception exception) {
				System.out.println(exception.getLocalizedMessage());
			}
		}
	}

}
