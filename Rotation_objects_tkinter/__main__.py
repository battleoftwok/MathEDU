from tkinter_app_pattern import TkinterApp
import tkinter as tk
import random
import math


class Rectangle:
    _canvas_ids = []

    def __init__(self, specific_canvas: tk.Canvas, coordinates: tuple, center: tuple):
        """
        Args:
            specific_canvas: полотно, на котором необходимо нарисовать прямоугольник

            coordinates: координаты вершин прямоугльника. Является кортежем, в котором расположено 4
                         кортежа (смотреть пример ниже), каждый из которых содержит координаты вершины
                         прямоугольника

            center: координата на полотне, совпадающая с центром прямоугольника.
        Examples:
            >>> your_canvas = tk.Canvas(tk.Tk(), width=720, height=720)
            >>> new_rect = Rectangle(your_canvas, (-40, -40, -40, 40, 40, 40, 40, -40), (5, 10))
        """

        self.canvas = specific_canvas  # назвал specific_canvas, чтобы линтер не доставал.
        self.coordinates = coordinates
        self.operable_center = center

        # корректировка введённых координат:
        self.correcting_coordinates = [(self.operable_center[0] + coord, self.operable_center[1] - coord)
                                       for coord in self.coordinates]

    def draw(self, **rect_params):
        self._canvas_ids.append(self.canvas.create_polygon(self.correcting_coordinates, **rect_params))

    def rotation(self, delta_: int, plus, **rect_params):
        angle_in_radians = delta_ * math.pi / 180  # перевод градусов в радианы
        # Матрица вращения:
        matrix_rot = [math.cos(angle_in_radians), -math.sin(angle_in_radians),
                      math.sin(angle_in_radians), math.cos(angle_in_radians)]

        # Расчёт новых координат вершин прямоугольника с учётом угла поворота:
        new_coordinates = [
            (self.coordinates[2 * i] * matrix_rot[0] + self.coordinates[2 * i + 1] * matrix_rot[1] + plus,
             self.coordinates[2 * i] * matrix_rot[2] + self.coordinates[2 * i + 1] * matrix_rot[3] + plus)
            for i in range(4)]

        # Удаляем с полотна старый прямоугольник:
        self.canvas.delete(self._canvas_ids)

        # Отрисовка повёрнутого прямоугольника:
        self._canvas_ids = [self.canvas.create_polygon([(self.operable_center[0] + new_coordinates[i][0],
                                                         self.operable_center[1] - new_coordinates[i][1])
                                                        for i in range(4)],
                                                       **rect_params)]

    @property
    def canvas_center(self):
        return int(self.canvas['width']) // 2, int(self.canvas['height']) // 2


class App(TkinterApp):
    angle_rotation = 1  # угол вращения
    rotational_velocity = 100  # скорость изменения угла вращения
    offset = 0  # смещение центра вращения

    def _ready(self):
        self.canvas = tk.Canvas(self.root, width=720, height=720)
        self.canvas.pack()

        self.root.bind('<Right>', self.up_rotational_velocity)
        self.root.bind('<Left>', self.down_rotational_velocity)
        self.root.bind('<Up>', self.up_plus)
        self.root.bind('<Down>', self.down_plus)

        self.my_coordinates = (-100 + self.offset, -100 + self.offset,
                               -100 + self.offset, 100 + self.offset,
                               100 + self.offset, 100 + self.offset,
                               100 + self.offset, -100 + self.offset)

        self.my_center = (360, 360)

        # первый прямоугольник
        self.rect = Rectangle(self.canvas, self.my_coordinates, self.my_center)

        self.new_coordinates = (-200 + self.offset, -200 + self.offset,
                                -200 + self.offset, 200 + self.offset,
                                200 + self.offset, 200 + self.offset,
                                200 + self.offset, -200 + self.offset)

        self.new_center = (360, 360)

        # второй прямоугольник
        self.new_rect = Rectangle(self.canvas, self.new_coordinates, self.new_center)

        self.third_coordinates = (-100 + self.offset, -100 + self.offset,
                                  -100 + self.offset, 100 + self.offset,
                                  100 + self.offset, 100 + self.offset,
                                  100 + self.offset, -100 + self.offset)

        self.third_center = (360, 360)

        # второй прямоугольник
        self.third_rect = Rectangle(self.canvas, self.third_coordinates, self.third_center)

        self.third_coordinates = (-100 + self.offset, -100 + self.offset,
                                  -100 + self.offset, 100 + self.offset,
                                  100 + self.offset, 100 + self.offset,
                                  100 + self.offset, -100 + self.offset)

        self.third_center = (360, 360)

        # второй прямоугольник
        self.third_rect = Rectangle(self.canvas, self.third_coordinates, self.third_center)

    def up_rotational_velocity(self, event):
        self.rotational_velocity += 1

    def down_rotational_velocity(self, event):
        self.rotational_velocity -= 1

    def up_plus(self, event):
        self.offset += 5

    def down_plus(self, event):
        self.offset -= 5

    def motion(self):
        self.angle_rotation += self.rotational_velocity

    def _physics_process(self, delta):
        self.motion()

    def _draw(self):
        # self.rect.rotation(self.angle_rotation, 200 * math.sin(10 * self.angle_rotation),
        #                    fill=self.get_random_hex_color())
        self.new_rect.rotation(self.angle_rotation, 0, fill='#4096C1')
        self.third_rect.rotation(-self.angle_rotation, 0,
                                 fill='#FFB55C')

    @staticmethod
    def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
        return '#%.2x%.2x%.2x' % (random.randint(*red_limit), random.randint(*green_limit), random.randint(*blue_limit))


if __name__ == '__main__':
    app = App()
    app.run()
