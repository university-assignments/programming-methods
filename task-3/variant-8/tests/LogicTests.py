# tests/LogicTests.py
import unittest
import math
from app.logic import TriangleLogic


class LogicTests(unittest.TestCase):
	def test_calculate_area(self):
		# Прямоугольный треугольник
		points = [(0, 0), (3, 0), (0, 4)]
		self.assertAlmostEqual(TriangleLogic.calculate_area(points), 6.0)

		# Вырожденный треугольник
		points = [(0, 0), (2, 2), (1, 1)]
		self.assertEqual(TriangleLogic.calculate_area(points), 0.0)

		# Отрицательные координаты
		points = [(-1, -1), (2, 3), (4, -3)]
		expected = 0.5 * abs((2 + 1) * (-3 + 1) - (3 + 1) * (4 + 1))
		self.assertAlmostEqual(TriangleLogic.calculate_area(points), expected)

	def test_calculate_sides(self):
		points = [(0, 0), (3, 0), (0, 4)]
		a, b, c = TriangleLogic.calculate_sides(points)
		self.assertAlmostEqual(a, 5.0)  # Гипотенуза
		self.assertAlmostEqual(b, 4.0)
		self.assertAlmostEqual(c, 3.0)

		# Равносторонний треугольник
		points = [(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]
		a, b, c = TriangleLogic.calculate_sides(points)
		self.assertAlmostEqual(a, 1.0)
		self.assertAlmostEqual(b, 1.0)
		self.assertAlmostEqual(c, 1.0)

	def test_calculate_angles(self):
		# Прямоугольный треугольник
		angles = TriangleLogic.calculate_angles(5.0, 4.0, 3.0)
		self.assertAlmostEqual(angles[0], 90.0, delta=1e-6)
		self.assertAlmostEqual(angles[1], 53.130102, delta=1e-6)
		self.assertAlmostEqual(angles[2], 36.869898, delta=1e-6)

		# Равносторонний треугольник
		angles = TriangleLogic.calculate_angles(1.0, 1.0, 1.0)
		for angle in angles:
			self.assertAlmostEqual(angle, 60.0, delta=1e-6)

	def test_determine_type(self):
		# Равносторонний
		angles = [60.0, 60.0, 60.0]
		type_str = TriangleLogic.determine_type(1.0, 1.0, 1.0, angles)
		self.assertIn("Равносторонний", type_str)

		# Равнобедренный + прямоугольный
		angles = [90.0, 45.0, 45.0]
		type_str = TriangleLogic.determine_type(math.sqrt(2), 1.0, 1.0, angles)
		self.assertIn("Равнобедренный", type_str)
		self.assertIn("Прямоугольный", type_str)

		# Тупоугольный
		angles = [100.0, 40.0, 40.0]
		type_str = TriangleLogic.determine_type(5.0, 3.0, 3.0, angles)
		self.assertIn("Тупоугольный", type_str)

	def test_calculate_circumradius(self):
		# Прямоугольный треугольник
		radius = TriangleLogic.calculate_circumradius(5.0, 4.0, 3.0, 6.0)
		self.assertAlmostEqual(radius, 2.5)  # R = c/2

		# Равносторонний треугольник
		side = 2.0
		area = (math.sqrt(3) / 4) * side ** 2
		radius = TriangleLogic.calculate_circumradius(side, side, side, area)
		self.assertAlmostEqual(radius, side / math.sqrt(3), delta=1e-6)

	def test_calculate_heights(self):
		# Прямоугольный треугольник (3-4-5)
		ha, hb, hc = TriangleLogic.calculate_heights(5.0, 4.0, 3.0, 6.0)
		self.assertAlmostEqual(ha, 2.4)  # 2*6/5
		self.assertAlmostEqual(hb, 3.0)  # 2*6/4
		self.assertAlmostEqual(hc, 4.0)  # 2*6/3

		# Вырожденный треугольник
		ha, hb, hc = TriangleLogic.calculate_heights(0.0, 2.0, 3.0, 0.0)
		self.assertEqual(ha, 0.0)
		self.assertEqual(hb, 0.0)
		self.assertEqual(hc, 0.0)


if __name__ == '__main__':
	unittest.main()
