# app/storage.py
import os
from pathlib import Path
from typing import List


class StorageException(Exception):
	"""Базовое исключение для ошибок хранилища"""
	DEFAULT_MSG = "Ошибка работы с хранилищем"

	def __init__(self, message: str = None):
		self.message = message or self.DEFAULT_MSG
		super().__init__(self.message)

class FileNotFoundError(StorageException):
	DEFAULT_MSG = "Файл не найден"

class PermissionError(StorageException):
	DEFAULT_MSG = "Нет прав доступа к файлу"

class InvalidDataError(StorageException):
	DEFAULT_MSG = "Некорректные данные в файле"

class InsufficientPointsError(StorageException):
	DEFAULT_MSG = "Недостаточно точек для построения треугольника"

class Storage:
	def __init__(self, root_path: str = "storage"):
		self._root_path = Path(root_path)
		self._file_names: List[str] = []
		self.get_all_files()

	@property
	def root_path(self) -> str:
		return str(self._root_path)

	@property
	def file_names(self) -> List[str]:
		return self._file_names

	def get_all_files(self) -> None:
		self._file_names = [
			f.name for f in self._root_path.iterdir()
			if f.is_file() and f.suffix == ".txt"
		]

	def read_file(self, file_name: str) -> list[tuple[float, float]]:
		file_path = self._root_path / file_name
		try:
			if not file_path.exists():
				raise FileNotFoundError(f"Файл {file_name} не существует")

			if not os.access(file_path, os.R_OK):
				raise PermissionError(f"Нет прав на чтение файла {file_name}")

			with file_path.open() as f:
				points = []
				for line_num, line in enumerate(f, 1):
					line = line.strip()
					if not line:
						continue

					try:
						x, y = map(float, line.split())
						points.append((x, y))
					except ValueError as e:
						raise InvalidDataError(
							f"Ошибка в строке {line_num}: {e}\nСодержимое строки: '{line}'"
						) from e

				if len(points) < 3:
					raise InsufficientPointsError(
						f"Найдено только {len(points)} точек. Требуется 3"
					)
				return points[:3]  # Берем первые 3 точки если их больше

		except StorageException:
			raise  # Пробрасываем наши исключения дальше
		except Exception as e:
			raise StorageException(f"Неизвестная ошибка: {str(e)}") from e
