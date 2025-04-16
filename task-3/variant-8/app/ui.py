# app/ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from storage import Storage, StorageException, FileNotFoundError, PermissionError, InvalidDataError, InsufficientPointsError
from logic import TriangleLogic


class TriangleApp:
	def __init__(self):
		self.root = tk.Tk()
		self.storage = Storage()
		self.current_points: Optional[list[tuple[float, float]]] = None
		self.create_widgets()

	def run(self):
		self.root.mainloop()

	def create_widgets(self):
		self.root.title("Triangle Analyzer")
		self.root.geometry("800x600")

		# Main container
		main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
		main_paned.pack(fill=tk.BOTH, expand=True)

		# Storage panel (30%)
		storage_frame = ttk.Frame(main_paned, width=240)
		self.build_storage_panel(storage_frame)
		main_paned.add(storage_frame)

		# Right panel (70%)
		right_paned = ttk.PanedWindow(main_paned, orient=tk.VERTICAL)

		# Draw panel (50%)
		draw_frame = ttk.Frame(right_paned)
		self.canvas = tk.Canvas(draw_frame, bg='white')
		self.canvas.pack(fill=tk.BOTH, expand=True)
		right_paned.add(draw_frame)

		# Info panel (50%)
		info_frame = ttk.Frame(right_paned)
		self.info_text = tk.Text(info_frame, wrap=tk.WORD)
		self.info_text.pack(fill=tk.BOTH, expand=True)
		right_paned.add(info_frame)

		main_paned.add(right_paned)

	def build_storage_panel(self, parent: ttk.Frame):
		listbox = tk.Listbox(parent)
		scrollbar = ttk.Scrollbar(parent)

		for fname in self.storage.file_names:
			listbox.insert(tk.END, fname)

		listbox.bind('<<ListboxSelect>>', self.on_file_select)
		listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		listbox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=listbox.yview)

	def on_file_select(self, event):
		widget = event.widget
		selection = widget.curselection()

		if not selection:
			return

		file_name = widget.get(selection[0])
		try:
			points = self.storage.read_file(file_name)
			self.current_points = points
			self.analyze_and_display()

		except FileNotFoundError as e:
			self.show_error("Ошибка файла", e.message)
		except PermissionError as e:
			self.show_error("Ошибка доступа", e.message)
		except InvalidDataError as e:
			self.show_error("Ошибка данных", e.message)
		except InsufficientPointsError as e:
			self.show_error("Недостаточно данных", e.message)
		except StorageException as e:
			self.show_error("Ошибка хранилища", e.message)
		except Exception as e:
			self.show_error("Критическая ошибка", f"Необработанное исключение: {str(e)}")

	def show_error(self, title: str, message: str):
		self.clear_display()
		messagebox.showerror(title, message)
		self.root.update_idletasks()  # Обновляем интерфейс

	def analyze_and_display(self):
		if not self.current_points:
			return

		try:
			area = TriangleLogic.calculate_area(self.current_points)
			if area == 0:
				raise ValueError("Degenerate triangle")

			a, b, c = TriangleLogic.calculate_sides(self.current_points)
			angles = TriangleLogic.calculate_angles(a, b, c)

			buffer = (
				f"Тип: {TriangleLogic.determine_type(a, b, c, angles)}",
				f"Углы: {angles[0]:.2f}°, {angles[1]:.2f}°, {angles[2]:.2f}°",
				f"Радиус описанной окружности: {TriangleLogic.calculate_circumradius(a, b, c, area):.2f}",
				f"",
				f"Высоты:",
				f"    ha = {TriangleLogic.calculate_heights(a, b, c, area)[0]:.2f}",
				f"    hb = {TriangleLogic.calculate_heights(a, b, c, area)[1]:.2f}",
				f"    hc = {TriangleLogic.calculate_heights(a, b, c, area)[2]:.2f}"
			)

			self.info_text.delete(1.0, tk.END)
			self.info_text.insert(tk.END, '\n'.join(buffer))
			self.draw_triangle()

		except Exception as e:
			messagebox.showerror("Error", str(e))
			self.clear_display()

	def draw_triangle(self):
		self.canvas.delete("all")
		if not self.current_points:
			return

		# Get canvas dimensions
		canvas_width = self.canvas.winfo_width()
		canvas_height = self.canvas.winfo_height()
		padding = 20

		# Extract coordinates
		x_coords = [p[0] for p in self.current_points]
		y_coords = [p[1] for p in self.current_points]

		# Calculate bounding box
		min_x, max_x = min(x_coords), max(x_coords)
		min_y, max_y = min(y_coords), max(y_coords)

		# Calculate scaling factors
		if (max_x - min_x) == 0 or (max_y - min_y) == 0:
			scale = 1.0
		else:
			scale_x = (canvas_width - 2 * padding) / (max_x - min_x)
			scale_y = (canvas_height - 2 * padding) / (max_y - min_y)
			scale = min(scale_x, scale_y)

		# Calculate center point
		center_x = (min_x + max_x) / 2
		center_y = (min_y + max_y) / 2

		# Transform coordinates
		def transform(x: float, y: float) -> tuple[float, float]:
			tx = (x - center_x) * scale + canvas_width // 2
			ty = (y - center_y) * scale + canvas_height // 2
			return tx, ty

		# Draw transformed triangle
		transformed = [transform(x, y) for (x, y) in self.current_points]
		self.canvas.create_polygon(
			transformed[0][0], transformed[0][1],
			transformed[1][0], transformed[1][1],
			transformed[2][0], transformed[2][1],
			fill='#e0e0ff', outline='black', width=2
		)

	def clear_display(self):
		self.canvas.delete("all")
		self.info_text.delete(1.0, tk.END)
