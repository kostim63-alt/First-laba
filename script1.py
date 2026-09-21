import numpy as np
from PIL import Image
from math import floor

SCALE = 8000
SHIFT_X = 500
SHIFT_Y = 900

def draw_dot(img_mat, x, y):# Рисуем точки с масштабированием, но бес сдвигания
    img_mat[-1 * floor(y) + SHIFT_Y, floor(x) + SHIFT_X, 0] = 255
    img_mat[-1 * floor(y) + SHIFT_Y, floor(x) + SHIFT_X, 1] = 255
    img_mat[-1 * floor(y) + SHIFT_Y, floor(x) + SHIFT_X, 2] = 255
    return

def draw_line(img_mat, x0, y0, x1, y1):
    x_change = abs((floor(x1) - floor(x0)))
    y_change = abs((floor(y1) - floor(y0)))

    d_max = max(x_change, y_change)
    L = d_max + 1

    if L == 1:
        draw_dot(img_mat, x0, y0)
        return

    d_x = (x1 - x0) / (L - 1)
    d_y = (y1 - y0) / (L - 1)

    for _ in range(L):
        draw_dot(img_mat, x0, y0)# Используем специальный метод для рисования точек

        x0 += d_x
        y0 += d_y

    return

v = []
f = []


with open("model.obj") as file:
    for i in file.readlines():
        spl = i.strip().split(' ')

        if spl[0] == 'v':
            v.append([float(x) * SCALE for x in spl[1:4]])
        elif spl[0] == 'f':
            f.append([int(x.split('/')[0]) - 1 for x in spl[1:4]])

img_mat_1 = np.zeros((1000, 1000, 3), dtype = np.uint8)

#for dot in v:
#    img_mat_1[floor(-1 * dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 0] = 255
#    img_mat_1[floor(-1 *dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 1] = 255
#    img_mat_1[floor(-1 * dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 2] = 255

for line in f:
    draw_line(img_mat_1, v[line[0]][0], v[line[0]][1], v[line[1]][0], v[line[1]][1])
    draw_line(img_mat_1, v[line[1]][0], v[line[1]][1], v[line[2]][0], v[line[2]][1])
    draw_line(img_mat_1, v[line[0]][0], v[line[0]][1], v[line[2]][0], v[line[2]][1])

img = Image.fromarray(img_mat_1)
img.save('img.png')