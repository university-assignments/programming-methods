# app/logic.py
import math


class TriangleLogic:
	@staticmethod
	def calculate_area(points: list[tuple[float, float]]) -> float:
		(x1, y1), (x2, y2), (x3, y3) = points
		return 0.5 * abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))

	@staticmethod
	def calculate_sides(points: list[tuple[float, float]]) -> tuple[float, float, float]:
		(x1, y1), (x2, y2), (x3, y3) = points
		return (
			math.hypot(x3 - x2, y3 - y2),
			math.hypot(x3 - x1, y3 - y1),
			math.hypot(x2 - x1, y2 - y1)
		)

	@staticmethod
	def calculate_angles(a: float, b: float, c: float) -> list[float]:
		# Вычисляем первые два угла
		angle_a = math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) if b * c != 0 else 0.0)
		angle_b = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)) if a * c != 0 else 0.0)

		# Третий угол вычисляем через сумму углов треугольника
		angle_c = 180.0 - angle_a - angle_b
		return [angle_a, angle_b, angle_c]

	@staticmethod
	def determine_type(a: float, b: float, c: float, angles: list[float]) -> str:
		types = []
		if math.isclose(a, b, rel_tol=1e-6) and math.isclose(b, c, rel_tol=1e-6):
			types.append("Равносторонний")
		elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
			types.append("Равнобедренный")

		if any(math.isclose(angle, 90, abs_tol=1e-6) for angle in angles):
			types.append("Прямоугольный")
		elif any(angle > 90 for angle in angles):
			types.append("Тупоугольный")
		else:
			types.append("Остроугольный")
		return ", ".join(types)

	@staticmethod
	def calculate_circumradius(a: float, b: float, c: float, area: float) -> float:
		return (a * b * c) / (4 * area) if area != 0 else 0.0

	@staticmethod
	def calculate_heights(a: float, b: float, c: float, area: float) -> tuple[float, float, float]:
		return (
			2 * area / a if a != 0 else 0.0,
			2 * area / b if b != 0 else 0.0,
			2 * area / c if c != 0 else 0.0
		)
