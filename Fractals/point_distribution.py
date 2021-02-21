import tkinter as tk
import random
import math


class Distribution:
    width = 720
    height = 720

    _canvas_axes_id = []
    _canvas_points_id = []

    complex_plus = 0

    def __init__(self, spread_radius: int = 50, amount_points: int = 1000):
        self.amount_points = amount_points
        self.spread_radius = spread_radius

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()

        self.root.bind('<Right>', self.right_plus)
        self.root.bind('<Left>', self.left_plus)

        # рисуем оси:
        self._draw_point()
        self._draw_axes()

    def left_plus(self, event):
        self.complex_plus -= -(.01 + .01j)
        for canvas_id in self._canvas_points_id:
            self.canvas.delete(canvas_id)
        self._canvas_points_id = []
        self._draw_point()

    def right_plus(self, event):
        self.complex_plus += -(.01 + .01j)
        for canvas_id in self._canvas_points_id:
            self.canvas.delete(canvas_id)
        self._canvas_points_id = []
        self._draw_point()

    def _draw_axes(self):
        self._canvas_axes_id = [
            self.canvas.create_line(self.width // 2, 0, self.width // 2, self.height),
            self.canvas.create_line(0, self.height // 2, self.width, self.height // 2)]

    def _draw_point(self):
        angle_list = []

        for angle in range(-180, 180, 1):
            angle_in_radians = angle * math.pi / 180  # перевод градусов в радианы

            complex_num = (complex((math.cos(angle_in_radians) + self.complex_plus),
                                   (math.sin(angle_in_radians) + self.complex_plus))) ** 2

            angle_list.append((self.size_adjustment((complex_num.real, complex_num.imag))))

            # print(complex_num)

        # print(angle_list)
        self._canvas_points_id = [self.canvas.create_polygon(*angle_list)]

    def size_adjustment(self, coordinates: tuple):
        return self.width // 2 + self.spread_radius * coordinates[0], \
               self.width // 2 - self.spread_radius * coordinates[1]

    def run(self):
        self.root.mainloop()

    @staticmethod
    def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
        return '#%.2x%.2x%.2x' % (random.randint(*red_limit), random.randint(*green_limit), random.randint(*blue_limit))


if __name__ == '__main__':
    dist = Distribution()

    dist.run()
