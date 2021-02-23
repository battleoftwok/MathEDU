import tkinter as tk
from random import randint


CANVAS_OPTIONS = {
    'width': 1020,
    'height': 1020,
    'bg': 'black'
}


def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
    return '#%.2x%.2x%.2x' % (randint(*red_limit), randint(*green_limit), randint(*blue_limit))


START_POINTS = [
    (CANVAS_OPTIONS['width'] / 2, CANVAS_OPTIONS['height'] / 5),
    (CANVAS_OPTIONS['width'] / 5, CANVAS_OPTIONS['height'] * 4 / 5),
    (CANVAS_OPTIONS['width'] * 4 / 5, CANVAS_OPTIONS['height'] * 4 / 5)
]

current_point = randint(0, CANVAS_OPTIONS['width']), randint(0, CANVAS_OPTIONS['height'])


def draw_point(xy, color='white', radius=5):
    x, y = xy
    canvas.create_oval(x, y, x, y, width=radius, outline=color)


def center(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return (x1 + x2) / 2, (y1 + y2) / 2


def process():
    global current_point
    root.after(1, process)
    target_point_no = randint(0, len(START_POINTS) - 1)
    current_point = center(current_point, START_POINTS[target_point_no])
    draw_point(current_point, color=get_random_hex_color())


root = tk.Tk()

canvas = tk.Canvas(root, **CANVAS_OPTIONS)
canvas.pack()

process()

root.mainloop()
