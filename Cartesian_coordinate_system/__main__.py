from tkinter import *
from tkinter.ttk import *
from tkinter.colorchooser import askcolor
import random
import time
import math


# https://www.youtube.com/watch?v=DxntHp7-wbg&ab_channel=VertDider - видео, которое вдохновило на написание данного кода



class App:
    _time_stamp = None
    _physics_flag = True
    side_a = 9
    side_b = 9

    coords = []
    list_prime_num = []
    objects = []
    drawning_color = 'yellow'
    bg = 'black'
    all_font_size = 12

    func_no = 1

    def __init__(self, width=900, height=900, func_no_plus=.0001, FPS=25):
        self.FPS = FPS
        self.width = width
        self.height = height
        self.func_no_plus = func_no_plus
        self.root = Tk()
        self.root.title('aniMath. Математические анимации')
        self.canvas = Canvas(self.root, width=width, height=height, bg=self.bg)

        self.draw_axes()
        self.draw_points(self.func_no)

        self.root.bind('<Right>', self.increase_variable)
        self.root.bind('<Left>', self.decrease_variable)

        self.color_frames = Frame(self.root)

        self.btn_background = Button(self.color_frames, text='background', command=self.fg_multicolored)
        self.btn_red = Button(self.color_frames, text='Красный', command=self._red_button)
        self.btn_green = Button(self.color_frames, text='Зелёный', command=self._green_button)
        self.btn_gray = Button(self.color_frames, text='Серый', command=self._gray_button)
        self.btn_yellow = Button(self.color_frames, text='Жёлтый', command=self._yellow_button)
        self.btn_black = Button(self.color_frames, text='Синий', command=self._blue_button)
        self.btn_lime = Button(self.color_frames, text='Лайм', command=self._lime_button)
        self.btn_random = Button(self.color_frames, text='Случайный', command=self._multicolored)
        self.btn_choose = Button(self.color_frames, text='Выбрать цвет', command=self.choose_drawning_color)

        self.btn_background.grid(row=0, column=0)
        self.btn_red.grid(row=0, column=1)
        self.btn_green.grid(row=1, column=0)
        self.btn_gray.grid(row=1, column=1)
        self.btn_yellow.grid(row=2, column=0)
        self.btn_black.grid(row=2, column=1)
        self.btn_lime.grid(row=3, column=0)
        self.btn_random.grid(row=3, column=1)
        self.btn_choose.grid(row=4, column=0, columnspan=10)

        self.btn_entry = Button(self.color_frames, text='Ввод', command=self._fix_step_and_FPS)
        self.btn_entry.grid(row=11, column=0, columnspan=10)

        Label(self.color_frames, text="", font=('Comic Sans MS', self.all_font_size)).grid(row=5, column=0,
                                                                                           columnspan=10)

        Label(self.color_frames, text="Параметры:", font=('Comic Sans MS', self.all_font_size)).grid(row=6, column=0,
                                                                                                     columnspan=10)

        Label(self.color_frames, text=f"Шаг({self.func_no_plus}):", font=('Comic Sans MS', self.all_font_size)).grid(
            row=7, column=0)
        self.entry = Entry(self.color_frames, width=10)
        self.entry.grid(row=7, column=1)

        Label(self.color_frames, text="FPS(25):", font=('Comic Sans MS', self.all_font_size)).grid(row=8, column=0)
        self.entry2 = Entry(self.color_frames, width=10)
        self.entry2.grid(row=8, column=1)

        self.color_frames.grid(row=0, column=11, rowspan=10)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

    def _fix_step_and_FPS(self):
        if self.entry.get() == '' and self.entry2.get() == '':
            self.func_no_plus = .001
            self.FPS = 25
        elif self.entry.get() == '':
            self.FPS = float(self.entry2.get())
        elif self.entry2.get() == '':
            self.func_no_plus = float(self.entry.get())
        else:
            self.FPS = float(self.entry2.get())
            self.func_no_plus = float(self.entry.get())

    def draw_axes(self):
        """
        Рисует координатные оси (без стрелочек) по середине холста
        """
        self.canvas.create_line(self.width / 2 + self.side_a / 2, 0, self.width / 2 + self.side_a / 2, self.height,
                                fill='gray')
        self.canvas.create_line(0, self.height / 2 + self.side_a / 2, self.width, self.height / 2 + self.side_a / 2,
                                fill='gray')

    def fg_multicolored(self):
        self.canvas['bg'] = askcolor()[1]

    def _red_button(self):
        self.drawning_color = 'red'

    def _multicolored(self):
        func = lambda: random.randint(0, 255)
        self.drawning_color = '#%02X%02X%02X' % (func(), func(), func())

    def _green_button(self):
        self.drawning_color = 'green'

    def _gray_button(self):
        self.drawning_color = 'gray'

    def _yellow_button(self):
        self.drawning_color = 'yellow'

    def _blue_button(self):
        self.drawning_color = 'blue'

    def _lime_button(self):
        self.drawning_color = 'lime'
        # self.drawning_color = 'lime'

    def choose_drawning_color(self):
        self.drawning_color = askcolor()[1]

    def choose_bg_color(self):
        self.bg = askcolor()[1]

    def draw_points(self, value):
        """
        Отрисовывает точки
        :param value: значение для расчёта значение функции в методе functions()
        """
        self.functions(value)
        for step in self.coords:
            self.objects.append(self.oval(*step, self.side_a, self.side_b, fill=self.drawning_color, width=2))

    def functions(self, val):
        """
        Функция, которую необходимо изобразить на холсте
        :param val: значение для расчёта функции
        """
        self.coords = []  # обнуление списка
        for step in range(0, self.width):
            self.coords.append(
                (.3 * step * math.e * math.sin(step * val), 0.3 * step * math.e * math.cos(step * val)))

            # TODO: Примеры других функций лежат в текстовом файле

    def run(self):
        """
        Запустить процесс
        """
        self._process()
        self.root.mainloop()

    def _process(self):
        self.root.after(round(1000 / self.FPS), self._process)

        if self._time_stamp is None:
            self._time_stamp = time.time()
            delta = 0
        else:
            delta = (time.time() - self._time_stamp) * 1000 / (1000 / self.FPS)
            self._time_stamp = time.time()

        if self._physics_flag:
            self._physics_process()

    def rectangle(self, start_x, start_y, side_width, side_height, **kwargs):
        """
        Отрисовывает такой же прямоугольник, что и метод create_rectangle, только в отличие от данного метода,
        вместо конечных координат указываются длины сторон прямоугольника.

        :param start_x: начальная координата x
        :param start_y: начальная координата y
        :param side_width: ширина прямоугольника (горизонтальная сторона прямоугольника)
        :param side_height: высота прямоугольника (вертикальная сторона прямоугольника)
        :param kwargs: остальные опции (можно добавлять все опции, которые есть у метода create_rectangle
        :return: прямоугольник координатами левого верхнего угла (start_x, start_y) и длинами сторон
        side_width, side_height.
        """
        return self.canvas.create_rectangle(start_x + self.width / 2,
                                            start_y + self.width / 2,
                                            start_x + self.width / 2 + side_width,
                                            start_y + self.width / 2 + side_height,
                                            **kwargs)

    def oval(self, start_x, start_y, side_width, side_height, **kwargs):
        """
        Отрисовывает такой же эллипс, что и метод create_oval, только в отличие от данного метода,
        вместо конечных координат указываются длины сторон прямоугольника, в который будет вписан эллипс.
        !!! Всегда отрисовывает

        :param start_x: начальная координата x
        :param start_y: начальная координата y
        :param side_width: ширина прямоугольника (горизонтальная сторона прямоугольника)
        :param side_height: высота прямоугольника (вертикальная сторона прямоугольника)
        :param kwargs: остальные опции (можно добавлять все опции, которые есть у метода create_rectangle
        :return: эллипс, вписанный в прямоугольник с координатами левого верхнего угла (start_x, start_y) и длинами
         сторон side_width, side_height.
        :return:
        """
        return self.canvas.create_oval(start_x + self.width / 2, start_y + self.width / 2,
                                       start_x + self.width / 2 + side_width,
                                       start_y + self.width / 2 + side_height,
                                       **kwargs)

    def _physics_process(self):
        self.canvas.delete(ALL)
        self.func_no += self.func_no_plus
        self.draw_points(self.func_no)
        self.draw_axes()

    def increase_variable(self, event):
        self.func_no_plus += 0.0001

    def decrease_variable(self, event):
        self.func_no_plus -= 0.0001

    @staticmethod
    def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
        return '#%.2x%.2x%.2x' % (random.randint(*red_limit), random.randint(*green_limit), random.randint(*blue_limit))


if __name__ == '__main__':
    app = App()
    app.run()
