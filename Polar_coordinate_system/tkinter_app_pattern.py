import tkinter as tk
import logging
import time
import configparser


class TkinterApp:
    """
    Класс приложения для tkinter.
    Автоматически вызываемые методы:
        _ready: единожды вызываемый метод, вызывается до вызова _process и до вызова Tk.mainloop
        _process: первый вызываемый метод, ничего не принимает, вызов безусловный
        _physics_process: второй вызываемый метод, принимает delta, ожидается bool или None
        _draw: последний вызываемый метод, вызывается если _physics_process вернул None или True
    """
    __regulator_FPS = __set_FPS = __current_FPS = 30
    __title = None
    __time_stamp = None
    __process_after = None
    _fps_stabilization = True

    def __init__(self, **tk_parameters):
        self.root = tk.Tk()
        self.root["bg"] = "black"

        self.log = logging.getLogger(f'{self.__class__.__name__} in {__file__}')
        self.config = configparser.ConfigParser()

        # установка всех параметров для окна tkinter
        for parameter_name in tk_parameters:
            self.root.__getattribute__(parameter_name)(tk_parameters[parameter_name])

        # проверка на существование методов и запрет/разрешение их запуска
        class_data = self.__dir__()
        self._ready_flag = '_ready' in class_data
        self._proc_flag = '_process' in class_data
        self._phys_flag = '_physics_process' in class_data
        self._draw_flag = '_draw' in class_data

        # в случае, если кокой-то метод отсутствует, пользователь будет уведомлен
        if not self._ready_flag:
            self.log.warning('метод _ready не обнаружен')
        if not self._proc_flag:
            self.log.warning('метод _process не обнаружен')
        if not self._phys_flag:
            self.log.warning('метод _physics_process не обнаружен')
        if not self._draw_flag:
            self.log.warning('метод _draw не обнаружен')

        self.log.info(f'инициализация {self.__class__.__name__} прошла успешно')

    def __str__(self):
        return f'{self.__class__.__name__}: {self.window_title}({self.window_width}, {self.window_height})'

    def run(self):
        self.__time_stamp = time.time()
        if self._ready_flag:
            self._ready()
        self.root.after(10, self.__process)
        self.log.info('запуск приложения')
        self.root.mainloop()

    def stop(self):
        self.root.after_cancel(self.__process_after)
        self.log.debug('приложение остановлено')

    def __process(self):
        self.__process_after = self.root.after(round(1000 / self.__regulator_FPS), self.__process)
        update = None
        delta = (time.time() - self.__time_stamp) * 1000 / (1000 / self.FPS)
        self.__time_stamp = time.time()
        if abs(self.FPS - self.__set_FPS) > self.__set_FPS / 100 and self._fps_stabilization:
            self.__regulator_FPS = min(self.__regulator_FPS + (self.__set_FPS - self.FPS) / 10, self.__set_FPS * 2)
        if abs(self.FPS - self.__set_FPS) > self.__set_FPS / 2 and self._fps_stabilization:
            self.log.warning('серьезное падение производительности')
        elif abs(self.FPS - self.__set_FPS) > self.__set_FPS / 2:
            self.log.warning('подозрительная активность системы стабилизации FPS')
        self.__current_FPS = self.FPS / (delta + 10**(-15))

        if self.fps_on_top:
            self.root.title(f'{self.__title}. FPS: {round(self.FPS)}')

        # вызов пользовательских методов
        if self._proc_flag:
            self._process()
        if self._phys_flag:
            update = self._physics_process(delta)
        if self._draw_flag:
            if update is not None:
                if update:
                    self._draw()
            else:
                self._draw()

    @property
    def fps_on_top(self):
        return self.__title is not None

    @fps_on_top.setter
    def fps_on_top(self, new_value: bool):
        if new_value:
            self.__title = self.window_title
        else:
            self.__title = None

    @property
    def FPS(self):
        return self.__current_FPS

    @FPS.setter
    def FPS(self, new_value):
        self.__set_FPS = new_value

    @property
    def window_width(self) -> int:
        return self.root.winfo_width()

    @window_width.setter
    def window_width(self, new_value: int):
        self.root.geometry(f'{new_value}x{self.window_height}')

    @property
    def window_height(self) -> int:
        return self.root.winfo_height()

    @window_height.setter
    def window_height(self, new_value: int):
        self.root.geometry(f'{self.window_width}x{new_value}')

    @property
    def window_center(self) -> tuple:
        return self.window_width / 2, self.window_height / 2

    @property
    def window_title(self) -> str:
        return self.root.title()

    @window_title.setter
    def window_title(self, new_value: str):
        self.root.title(new_value)
