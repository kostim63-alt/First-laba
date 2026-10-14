from random import randint

import numpy as np
from PIL import Image
from math import floor, ceil

SCALE = 8000
SHIFT_X = 500
SHIFT_Y = 900
size = (1000, 1000, 3)
buffer_size = (1000, 1000)

def correct_coordinates(x, y):
    y, x = -1 * y + SHIFT_Y, x + SHIFT_X

    return x, y

def draw_dot(img_mat, x, y, color):# Рисуем точки с масштабированием, но бес сдвигания
    img_mat[y, x, 0] = color[0]
    img_mat[y, x, 1] = color[1]
    img_mat[y, x, 2] = color[2]
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

def bc(x, y, x0, y0, x1, y1, x2, y2):

    low = ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))

    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / low
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / low
    lambda2 = 1.0 - lambda0 - lambda1

    return lambda0, lambda1, lambda2

def draw_triangle(img_mat, color, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    x_min = floor(max(min(x0, x1, x2), 0))
    y_min = floor(max(min(y0, y1, y2), 0))

    x_max = ceil(min(max(x0, x1, x2), 999))
    y_max = ceil(min(max(y0, y1, y2), 999))

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            l0, l1, l2 = bc(x + 0.5, y + 0.5, x0, y0, x1, y1, x2, y2)

            if(l0 >= 0 and l1 >= 0 and l2 >= 0):
                z = l0*z0 + l1*z1 + l2*z2

                if z < z_buffer[x][y]:
                    draw_dot(img_mat, x, y, color)
                    z_buffer[x][y] = z


def normal(x0, y0, z0, x1, y1, z1,  x2, y2, z2):
    return np.cross([x1 - x2, y1 - y2, z1 - z2], [x1 - x0, y1 - y0, z1 - z0])

v = []
f = []


with open(".venv/model.obj") as file:
     for i in file.readlines():
         spl = i.strip().split(' ')

         if spl[0] == 'v':
             v.append([float(x) * SCALE for x in spl[1:4]])
         elif spl[0] == 'f':
             f.append([int(x.split('/')[0]) - 1 for x in spl[1:4]])

img_mat_1 = np.zeros(size, dtype = np.uint8)

z_buffer = np.zeros(buffer_size)

for i in range(size[0]):
    for j in range(size[1]):
        z_buffer[i, j] = np.inf

# for dot in v:
#     img_mat_1[floor(-1 * dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 0] = 255
#     img_mat_1[floor(-1 *dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 1] = 255
#     img_mat_1[floor(-1 * dot[1] + SHIFT_Y), floor(dot[0] + SHIFT_X), 2] = 255

for line in f:
    x0, y0, z0 = v[line[0]][0], v[line[0]][1], v[line[0]][2]
    x1, y1, z1 = v[line[1]][0], v[line[1]][1], v[line[1]][2]
    x2, y2, z2 = v[line[2]][0], v[line[2]][1], v[line[2]][2]

    n = - normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    l = [0, 0, 1]



    scolar = np.dot(n, l) / np.linalg.norm(n) / np.linalg.norm(l)

    if scolar > 0:
        x0, y0 = correct_coordinates(x0, y0)
        x1, y1 = correct_coordinates(x1, y1)
        x2, y2 = correct_coordinates(x2, y2)

        color = [-255 * scolar, 0, 0]

        draw_triangle(img_mat_1, color, x0, y0, z0, x1, y1, z1, x2, y2, z2)


    # draw_line(img_mat_1, v[line[0]][0], v[line[0]][1], v[line[1]][0], v[line[1]][1])
    # draw_line(img_mat_1, v[line[1]][0], v[line[1]][1], v[line[2]][0], v[line[2]][1])
    # draw_line(img_mat_1, v[line[0]][0], v[line[0]][1], v[line[2]][0], v[line[2]][1])

img = Image.fromarray(img_mat_1)
img.save('img.png')
