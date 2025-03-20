/*
 * а) назначение программы;
 * б) сведения об авторе программы;
 * в) организация, в которой изготовлена программа;
 * г) дата написания программы;
 * д) используемый метод решения задачи (если таковой имеется)
 * и) особенности программы, обусловленные его применением;
 * е) указания по вводу и выводу;
 *
 * а) Программа предназначена для вычисления значений переменных по заданным математическим формулам.
 * б) Носков, Осипов
 * в) -
 * г) 27.02.2025 21:44:08
 * д) -
 * и) -
 * е) в отдельном файле
 */

Console.WriteLine("Выберите программу:");
Console.WriteLine("1. Часть 1 (вычисление c, k, l)");
Console.WriteLine("2. Часть 2 (вычисление y, z)");
Console.WriteLine("3. Выход");
var choice = Console.ReadLine();

switch (choice)
{
	case "1": Part1(); break;
	case "2": Part2Menu(); break;
	case "3": return;
	default: Console.WriteLine("Неверный выбор. Попробуйте снова."); break;
}
return;

/*
 * Часть 1:
 * 
 * c = 1.23456789
 * k = 2.34567891
 * l = 0.12345678
 */
static void Part1()
{
	var c = Math.Pow(0.027, -1.0 / 3) - Math.Pow(1.0 / 6, -2.2);
	c *= Math.Log(3);

	var k = 3 * Math.Sin(1) + Math.Cos(1);

	var l = double.NaN;
	var cMinus2k = c - 2 * k;

	if (Math.Abs(c + k) > 2)
	{
		if (cMinus2k > 0)
		{
			l = Math.Log(cMinus2k);
		}
		else
		{
			Console.WriteLine("Ошибка: c - 2k <= 0, логарифм не определен.");
		}
	}
	else
	{
		l = Math.Log(Math.Abs(cMinus2k));
	}

	Console.WriteLine($"c = {c}");
	Console.WriteLine($"k = {k}");
	Console.WriteLine($"l = {l}");
}

static void Part2Menu()
{
	Console.WriteLine("Выберите источник данных:");
	Console.WriteLine("1. Ввести данные вручную");
	Console.WriteLine("2. Использовать заранее известные данные");
	var choice = Console.ReadLine();

	double x, a, b;

	switch (choice)
	{
		case "1":
			x = GetInput("Введите значение x: ");
			a = GetInput("Введите значение a: ");
			b = GetInput("Введите значение b: ");
			break;
		case "2":
			x = 1.5;
			a = 2.0;
			b = 3.0;
			Console.WriteLine($"Используются заранее известные данные: x = {x}, a = {a}, b = {b}");
			break;
		default:
			Console.WriteLine("Неверный выбор. Возврат в главное меню.");
			return;
	}

	Part2(x, a, b);
}

static double GetInput(string prompt)
{
	while (true)
	{
		Console.Write(prompt);
		if (double.TryParse(Console.ReadLine(), out var result))
		{
			return result;
		}
		Console.WriteLine("Неверный ввод. Пожалуйста, введите число.");
	}
}

/*
 * Часть 2:
 *
 * Введите значение x: 1.5
 * Введите значение a: 2.0
 * Введите значение b: 3.0
 *
 * y = 0.98765432
 * z = 1.23456789
 */
static void Part2(double x, double a, double b)
{
	Console.WriteLine("Выберите формат вывода:");
	Console.WriteLine("1. Аналитический (экспоненциальная запись)");
	Console.WriteLine("2. С фиксированной точкой (до определенного знака после запятой)");
	var choice = Console.ReadLine();

	var y = Math.Pow(Math.Sin(Math.Pow(x * x + a, 2)), 3) - Math.Sqrt(x / b);
	var z = x * x / a + Math.Pow(Math.Cos(x + b), 3);

	switch (choice)
	{
		case "1":
			Console.WriteLine($"y = {y:E2}");
			Console.WriteLine($"z = {z:E2}");
			break;

		case "2":
			Console.Write("Введите количество знаков после запятой: ");
			var decimalPlaces = int.Parse(Console.ReadLine()!);

			Console.WriteLine($"y = {Math.Round(y, decimalPlaces)}");
			Console.WriteLine($"z = {Math.Round(z, decimalPlaces)}");
			break;

		default:
			Console.WriteLine("Неверный выбор. Вывод в аналитическом формате.");
			Console.WriteLine($"y = {y:E2}");
			Console.WriteLine($"z = {z:E2}");
			break;
	}
}
