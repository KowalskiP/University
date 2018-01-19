from tkinter import Tk, Canvas, PhotoImage, mainloop
import math

WIDTH, HEIGHT = 800, 600

MIN_X = 100000
MAX_X = -MIN_X
MAX_Y = MAX_X
MIN_Y = MIN_X

LEFT_X = -3
RIGHT_X = 3
LEFT_Y = -1
RIGHT_Y = 4

N = 500
M = WIDTH * 2


def f(x, y):
    return math.sin(x*y)


def isometric_x(x, y):
    return (y - x)*math.sqrt(3)/2


def isometric_y(x, y, z):
    return (x + y)/2 - z


def draw_graph():
    global MAX_X, MIN_X, MAX_Y, MIN_Y, N
    top = [0 for _ in range(M)]
    bottom = [0 for _ in range(M)]
    for i in range(N):
        x = RIGHT_X + i * (LEFT_X - RIGHT_X) / N
        for j in range(M):
            y = RIGHT_Y + j*(LEFT_Y - RIGHT_Y) / M
            z = f(x, y)
            xi = isometric_x(x, y)
            yi = isometric_y(x, y, z)
            if xi > MAX_X:
                MAX_X = xi
            if xi < MIN_X:
                MIN_X = xi
            if yi > MAX_Y:
                MAX_Y = yi
            if yi < MIN_Y:
                MIN_Y = yi

    for i in range(M):
        top[i] = HEIGHT
        bottom[i] = 0

    for i in range(N):
        x = RIGHT_X + i * (LEFT_X - RIGHT_X) / N
        for j in range(M):
            y = RIGHT_Y + j * (LEFT_Y - RIGHT_Y) / M
            z = f(x, y)
            xi = isometric_x(x, y)
            yi = isometric_y(x, y, z)
            xi = (xi - MIN_X) / (MAX_X - MIN_X) * WIDTH
            yi = (yi - MIN_Y) / (MAX_Y - MIN_Y) * HEIGHT
            if yi > bottom[int(xi)]:
                img.put("#ff0000", (int(xi), int(yi)))
                bottom[int(xi)] = int(yi)
            if yi < top[int(xi)]:
                img.put("#0000ff", (int(xi), int(yi)))
                top[int(xi)] = int(yi)

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

draw_graph()

mainloop()
