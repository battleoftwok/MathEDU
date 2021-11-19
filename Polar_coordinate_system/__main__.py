from abc import ABC, abstractmethod
from tkinter import Canvas
from tkinter_app_pattern import TkinterApp
import math as m
from random import randint
from PIL import Image, EpsImagePlugin

EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs9.55.0\bin\gswin64c.exe"

DIAPASON = 0, 11750


# http://grafikus.ru/examples/polar-functions - примеры графиков в полярных координатах


def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
    return '#%.2x%.2x%.2x' % (randint(*red_limit), randint(*green_limit), randint(*blue_limit))


class FunctionStrategy(ABC):

    @abstractmethod
    def convert_coords(self, coords: tuple):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, arg):
        raise NotImplementedError

    def __init__(self, width, height):
        self.height = height
        self.width = width


class DiapasonFunctionStrategy(FunctionStrategy, ABC):
    def __init__(self, width, height, diapason: tuple):
        super().__init__(width, height)
        self.diapason = diapason


class DekartFunctionStrategy(DiapasonFunctionStrategy, ABC):

    def convert_coords(self, coords: tuple):
        return coords[0] + self.width // 2, -coords[1] + self.height // 2

    @property
    def x_values(self):
        return (i / 100 for i in range(*self.diapason))


class PolarFunctionStrategy(DiapasonFunctionStrategy, ABC):
    def convert_coords(self, coords: tuple):
        return (-coords[0] * m.cos(coords[1]) + self.width // 2,
                -coords[0] * m.sin(coords[1]) + self.height // 2)

    @property
    def polar_angles(self):
        return (i * m.pi for i in range(*self.diapason))


class Parabola(DekartFunctionStrategy):
    def __call__(self, arg):
        coords = ((x, x ** 2) for x in self.x_values)
        return (self.convert_coords(coord) for coord in coords)


class ButterflyStrategy(PolarFunctionStrategy):

    def __call__(self, arg):
        foo = ((100 * (m.e ** m.sin(angle * arg) - 2 * m.cos(4 * angle) + (m.sin((2 * angle - m.pi) / 24)) ** 5), angle)
               for angle in self.polar_angles)
        return (self.convert_coords(coords) for coords in foo)


class HeartStrategy(PolarFunctionStrategy):

    def __call__(self, arg):
        foo = ((80 * (2 - 2 * m.sin(angle + arg) + m.sin(angle) * (abs(m.cos(angle)) ** .5) / (m.sin(angle) + 1.4)),
                angle)
               for angle in self.polar_angles)
        return (self.convert_coords(coords) for coords in foo)


class ArhimedSpiralStrategy(PolarFunctionStrategy):

    def __call__(self, arg):
        foo = ((2 * angle,  angle) for angle in self.polar_angles)
        return (self.convert_coords(coords) for coords in foo)


class Chart:
    marker_len = 10
    canvas_id = []
    arg = 1

    def __init__(self, function: FunctionStrategy, canvas: Canvas, color, axes=True, markers=False, amount_markers=10,
                 indent=50):
        """
        Конструктор (инициализация)
        Args:
            canvas: полотно, на котором необходимо изобразить график
            color: цвет осей
            markers: метки (рисуются если markers = True)
            amount_markers: кол-во меток (по умолчанию: 10)
            indent: отступ осей от краёв полотна
        """
        self.canvas = canvas
        self.color = color
        self.markers = markers
        self.indent = indent
        self.amount_markers = amount_markers
        self.axes = axes
        self.function = function

        self.canvas_width = int(self.canvas['width'])  # ширина полотна
        self.canvas_height = int(self.canvas['height'])  # высота полотна

        if axes:
            self._draw_axes()

        if markers:
            self._draw_markers()

    def draw_function(self, fill):
        """
        Рисовать график
        Args:
            fill: цвет линии
        """

        # Небольшая ремарка: если изменить create_line на create_polygon, то будет интересно)
        self.canvas_id = [self.canvas.create_line(*self.function(self.arg),
                                                  fill=fill, width=2)]

    def _draw_axes(self):
        """
        Отрисовка осей координат
        """
        self.canvas.create_line(self.indent, self.indent,
                                self.indent, self.canvas_height - self.indent,
                                fill=self.color, width=2)

        self.canvas.create_line(self.indent, self.canvas_height - self.indent,
                                self.canvas_width - self.indent, self.canvas_height - self.indent,
                                fill=self.color, width=2)

        self.canvas.create_line(self.canvas_width // 2, self.indent,
                                self.canvas_width // 2, self.canvas_height - self.indent, fill=self.color)

        self.canvas.create_line(self.indent, self.canvas_height // 2,
                                self.canvas_width - self.indent, self.canvas_height // 2, fill=self.color)

    def _draw_markers(self):
        """
        Отрисовка меток на осях
        """
        size_between_markers = (self.canvas_height - 2 * self.indent) // self.amount_markers
        for y in range(self.indent, self.canvas_height - self.indent + size_between_markers, size_between_markers):
            self.canvas.create_line(self.indent - self.marker_len, y,
                                    self.indent, y, fill=self.color, width=2)

        size_between_markers = (self.canvas_width - 2 * self.indent) // self.amount_markers
        for x in range(self.indent, self.canvas_width - self.indent + size_between_markers, size_between_markers):
            self.canvas.create_line(x, self.canvas_height - self.indent + self.marker_len,
                                    x, self.canvas_height - self.indent, fill=self.color, width=2)


class App(TkinterApp):
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': "black"
    }

    arg = 1
    plus = .01
    pause_flag = True

    def _ready(self):
        """
        Всё что указано в этом методе выполниться ровно один раз при запуске приложения
        Кнопки "стрелка вправо" и "стрелка влево" управляют скоростью изменения величины,
        которая фигурирует в уравнении (следовательно с помощью этих кнопок можно управлять
        скоростью воспроизведения анимации)
        """

        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        self.root.bind('<Right>', self.increase_variable)
        self.root.bind('<Left>', self.decrease_variable)
        self.root.bind('<space>', self.pause)
        self.root.bind('<Control-s>', self.save_picture)

        self.chart = Chart(Parabola(self.canvas_opts["width"], self.canvas_opts["height"], DIAPASON),
                           self.canvas, 'gray', markers=True)

    def save_picture(self, event):
        self.canvas.postscript(file="condition.ps", colormode="color")
        print("Состояние сохранено")
        img = Image.open("condition.ps")
        img.save("condition.png", "png")

    def pause(self, event):
        # if self.pause_flag:
        #     self.plus = 0
        #     self.pause_flag = False
        # elif self.pause_flag is False:
        #     self.plus = .01
        #     self.pause_flag = True

        self.chart.function = ArhimedSpiralStrategy(self.canvas_opts["width"], self.canvas_opts["height"], DIAPASON)

    def increase_variable(self, event):
        self.plus += .001

    def decrease_variable(self, event):
        self.plus -= .001

    def _physics_process(self, delta):
        self.clean_canvas()

        self.chart.arg += self.plus * delta

    def _draw(self):
        self.chart.draw_function("#EEBD08")

    def clean_canvas(self):
        """
        Метод, который очищает полотно (canvas) от элементов указанного списка.
        И очищает сам список от дескрипторов.
        """
        for canvas_obj in self.chart.canvas_id:
            self.canvas.delete(canvas_obj)
        self.chart.canvas_id = []


if __name__ == '__main__':
    app = App()
    app.run()
