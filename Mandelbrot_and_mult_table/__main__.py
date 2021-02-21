from tkinter import *
import time
import math

# https://www.youtube.com/watch?v=qhbuKbxJsk8&ab_channel=Mathologer - откуда узнал об этом, познавательное видео


class App:
    FPS = 30
    _time_stamp = None
    _physics_flag = True
    bg_canvas = 'black'
    side_a = 10
    side_b = 10
    cords_points = []
    amount_of_points = 100
    degree = 2
    delete_value = None
    dict_cords_points = {}
    output_list = []
    plus = 1
    float_list = []
    dict_cords_points_float = {}
    exp_list = []

    def __init__(self, width=900, height=900, radius=400):
        self.width = width
        self.height = height
        self.radius = radius

        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg=self.bg_canvas)

        self.root.bind('<Right>', self.button_right)
        self.root.bind('<Left>', self.button_left)
        self.root.bind('<Up>', self.button_up)
        self.root.bind('<Down>', self.button_down)
        self.root["bg"] = "black"

        # self.root.bind_all("<MouseWheel>", self.button_right)

        self.canvas.pack()

    def draw_oval(self, radius, **kwargs):
        """
        Отрисовка окжружности (круга) с заданным радиусом.

        :param radius: радиус окружности
        :param kwargs: остальные параметры, которые есть у метода create_rectangle
        :return: дескриптор (canvas id)
        """
        return self.canvas.create_oval((self.width - 2 * radius) // 2,
                                       (self.height - 2 * radius) // 2,
                                       self.width - (self.width - 2 * radius) // 2,
                                       self.height - (self.height - 2 * radius) // 2,
                                       **kwargs)

    def draw_axes(self, **kwargs):
        """
        Отрисовка осей

        :param kwargs: параметры, которые есть у метода create_line
        """
        self.canvas.create_line(self.width // 2, 0, self.width // 2, self.height, **kwargs)
        self.canvas.create_line(0, self.height // 2, self.width, self.height // 2, **kwargs)

    def calculation_of_coordinates(self):
        """
        Расчёт координат точек. Данная функция возвращает координаты, которые
        отрисуют точки ровно на линии окружности. Однако также в данном методе
        присутствует накопление списка cords_points координатами, соответствующими
        координатам окружности. И на основе этого списка генерируется словарь (dict)
        dict_cords_points, в котором каждая координата точки соотвествует её нумерации
        начиная с 0.
        """
        angle_in_degrees = 360 / (self.amount_of_points / self.plus)
        summa = 0

        for step in range(1, int(self.amount_of_points // self.plus) * 10 + 1):
            angle_in_radians = summa * math.pi / 180

            self.cords_points.append((self.radius * math.cos(angle_in_radians) + self.width // 2,
                                      self.radius * math.sin(angle_in_radians) + self.width // 2))

            summa += angle_in_degrees

        self.dict_cords_points = {number: cords for number, cords in
                                  zip(range(0, int(self.amount_of_points / self.plus)), self.cords_points)}

        self.exp_list = [self.cords_points]

    def draw_points(self, **kwargs):
        """
        Отрисовка точек на окружности равноудалённо.

        :param kwargs: параметры, которые есть у метода create_oval
        """
        angle_in_degrees = 360 / self.amount_of_points
        summa = 0

        for step in range(1, self.amount_of_points + 1):
            angle_in_radians = summa * math.pi / 180

            self.output_list.append((self.radius * math.cos(angle_in_radians) + self.width // 2 - self.side_a // 2,
                                     self.radius * math.sin(angle_in_radians) + self.width // 2 - self.side_b // 2,
                                     self.radius * math.cos(angle_in_radians) + self.height // 2 + self.side_a // 2,
                                     self.radius * math.sin(angle_in_radians) + self.height // 2 + self.side_b // 2))

            summa += angle_in_degrees

        for step in self.output_list:
            self.canvas.create_oval(step, **kwargs)

    def draw_lines(self, **kwargs):
        for i in self.dict_cords_points:
            if (i * self.degree) % (self.amount_of_points / self.plus) in self.dict_cords_points:
                self.canvas.create_line(self.dict_cords_points[i],
                                        self.dict_cords_points[(i * self.degree) % (self.amount_of_points / self.plus)],
                                        **kwargs)

    def button_left(self, event):
        self.degree = round(self.degree - self.plus, 8)

    def button_right(self, event):
        self.degree = round(self.degree + self.plus, 8)

    def button_up(self, event):
        self.amount_of_points += 1

    def button_down(self, event):
        if self.amount_of_points > 0:
            self.amount_of_points -= 1
        else:
            self.canvas.create_text(350, 320, text=f"Количество точек должно быть > 0!",
                                    fill="red", font=('Comic Sans MS', 30))

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

        self._draw()

    def _physics_process(self):
        self.canvas.delete(ALL)
        self.float_list = []
        self.cords_points = []
        self.dict_cords_points = {}
        self.output_list = []
        self.float_list = []
        self.dict_cords_points_float = {}
        self.exp_list = []
        self.calculation_of_coordinates()

    def _draw(self):
        self.draw_axes(fill='gray')
        self.draw_oval(self.radius, outline='red', width=3)
        self.draw_points(fill='yellow', outline='black')
        self.draw_lines(fill='#00FFFF', width=.1)
        self.canvas.create_text(150, 50, text=f"степень n = {self.degree}", fill="red",
                                font=('Comic Sans MS', 20, 'bold'))
        self.canvas.create_text(self.width - 150, 50, text=f"m точек = {self.amount_of_points}",
                                fill="red", font=('Comic Sans MS', 20, 'bold'))


if __name__ == '__main__':
    app = App()
    app.run()
