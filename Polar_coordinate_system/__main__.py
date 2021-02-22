from tkinter import Canvas
from tkinter_app_pattern import TkinterApp
import math as m

# http://grafikus.ru/examples/polar-functions - примеры графиков в полярных координатах


class Chart:
    marker_len = 10

    parameter_lists = {
        'list_angles': [],
        'list_radius': [],
        'list_coords': []
    }

    canvas_id = []

    def __init__(self, canvas: Canvas, color, axes=True, markers=False, amount_markers=10, indent=50):
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

        self.canvas_width = int(self.canvas['width'])  # ширина полотна
        self.canvas_height = int(self.canvas['height'])  # высота полотна

        if axes:
            self._draw_axes()

        if markers:
            self._draw_markers()

    def create_polar_angle(self):
        """
        В данном методе происходит заполнение списка значений полярных углов (в радианах)
        """
        for i in range(1, 1500):
            convert_radians = i * m.pi / 180
            self.parameter_lists['list_angles'].append(convert_radians)

    def create_polar_radius(self, arg):
        """
        В данном методе происходит заполнение списка значений полярных радиусов с учётом математического
        выражения (функции).
        Args:
            arg: изменяемая величина, которая позволяет отследить изменение графика,
                 если подставить её в математическое выражение (можно экспериментировать,
                 подставляя данную переменную в любую часть выражения, можно умножать на arg,
                 делить, прибавлять и т.д. При необходимости можно добавить новую переменную (например,
                 arg будет увеличиваться, а new_variable будет уменьшаться)).
        """
        for i in self.parameter_lists['list_angles']:
            self.parameter_lists['list_radius'].append(
                270 * m.cos(arg / i) * m.cos(arg * i))

        # Примеры других интересных функций:
        # 80 * (2 - 2 * m.sin(i + arg) + m.sin(i) * (abs(m.cos(i)) ** .5) / (m.sin(i) + 1.4))
        # 70 * (m.e ** m.sin(i) - 2 * m.cos(4 * i) + (m.sin((2 * i - m.pi) / 24)) ** 5))
        # 70 * (m.e ** m.sin(i * arg) - 2 * m.cos(4 * arg) + (m.sin((2 * i - m.pi) / arg)) ** 5))
        # 180 * m.sin(arg * m.e ** m.sin(i / arg) * m.e ** m.cos(i ** (1 / arg)))
        # 180 * m.sin(arg * m.e ** m.sin(i / arg) * m.e ** m.cos(i / arg))
        # 80 * (2 + 7 * m.cos(m.sin(i) + m.sin(arg * i)) * m.cos(i))
        # 200 * m.sin(arg * i - 10 * arg) * m.cos(i)
        # 300 * (m.sin(i * arg) // arg)
        # 270 * m.sin(arg / i) * m.cos(arg * i)

    def create_final_coord_list(self):
        """
        Заполнение списка окончательно посчитанными координатами. По ним будет строиться график.
        (заполнение происходит с корректировкой координат по Canvas)
        """
        for i, j in zip(self.parameter_lists['list_radius'], self.parameter_lists['list_angles']):
            self.parameter_lists['list_coords'].append(
                (-i * m.cos(j) + self.canvas_width // 2, -i * m.sin(j) + self.canvas_height // 2))

    def draw_function(self, fill):
        """
        Рисовать график
        Args:
            fill: цвет линии
        """

        # Небольшая ремарка: если изменить create_line на create_polygon, то будет интересно)
        self.canvas_id = [self.canvas.create_line(*self.parameter_lists['list_coords'], fill=fill, width=2)]

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

    def clean_canvas(self, clean_list: list):
        """
        Метод, который очищает полотно (canvas) от элементов указанного списка.
        И очищает сам список от дескрипторов.
        Args:
            clean_list:
        """
        for canvas_obj in clean_list:
            self.canvas.delete(canvas_obj)
        clean_list = []


class App(TkinterApp):
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    arg = 1
    plus = .01

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

        self.chart = Chart(self.canvas, 'yellow', markers=True)

        self.chart.create_polar_angle()
        self.chart.create_polar_radius(self.arg)
        self.chart.create_final_coord_list()
        self.chart.draw_function('red')

    def increase_variable(self, event):
        self.plus += .001

    def decrease_variable(self, event):
        self.plus -= .001

    def _physics_process(self, delta):
        self.chart.parameter_lists['list_radius'] = []
        self.chart.parameter_lists['list_coords'] = []
        self.chart.clean_canvas(self.chart.canvas_id)

        self.arg += self.plus

        self.chart.create_polar_radius(self.arg)
        self.chart.create_final_coord_list()

    def _draw(self):
        self.chart.draw_function('red')


if __name__ == '__main__':
    app = App()
    app.run()
