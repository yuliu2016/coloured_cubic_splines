import sys

import numpy as np
import pygame

SIZE = W, H = (495, 493)
pygame.init()
display = pygame.display.set_mode(SIZE)
changed = True


class CubicSpline:
    def __init__(self, p0, m0, p1, m1):
        self._a = 2 * p0 - 2 * p1 + m0 + m1
        self.b = -2 * m0 - m1 - 3 * p0 + 3 * p1
        self.c = m0
        self.d = p0

    def __getitem__(self, t):
        return 1 * self._a * t ** 3 + self.b * t ** 2 + self.c * t + self.d

    def v(self, t):
        return 3 * self._a * t ** 2 + 2 * self.b * t + self.c

    def a(self, t):
        return 6 * self._a * t + 2 * self.b

    def j(self):
        return 6 * self._a


def spline_seg(p0, m0, p1, m1):
    pts = list(zip(p0, m0, p1, m1))
    return CubicSpline(*pts[0]), CubicSpline(*pts[1])


display.fill((255, 255, 255))

img = pygame.image.load("field.PNG")
display.blit(img, (0, 0))


def tx(ox):
    return ox + 247


def ty(oy):
    return 493 - oy


def lc(c):
    if c > 255:
        return 255
    if c < 0:
        return 0
    return int(c)


def lint(a, b, x):
    return a + (b - a) * x


def ic(c1, c2, x):
    return lint(c1[0], c2[0], x), lint(c1[1], c2[1], x), lint(c1[2], c2[2], x)


def draw(c, d, tp):
    xs, ys, = tp
    lx = xs[0]
    ly = ys[0]
    a = 200
    if d:
        a = 30
    c_min = (lc(256 - c[0] * 0.5), lc(256 - c[1] * 0.5), lc(256 - c[2] * 0.5))
    k_min = 1
    k_max = 0
    pt = []

    for i in np.linspace(0, 1, a):
        xi = xs[i]
        yi = ys[i]
        nx = int(xi)
        ny = int(yi)
        xvi = xs.v(i)
        yvi = ys.v(i)
        k = abs(xvi * ys.a(i) - yvi * xs.a(i)) / (xvi ** 2 + yvi ** 2) ** 1.5
        if k < k_min:
            k_min = k
        if k > k_max:
            k_max = k
        pt.append(((tx(ly), ty(lx)), (tx(ny), ty(nx)), k))
        lx = nx
        ly = ny

    for f, t, k in pt:
        fc = ic(c, c_min, (k - k_min) / (k_max - k_min))
        if d:
            pygame.draw.circle(display, fc, t, 2)
        else:
            pygame.draw.line(display, fc, f, t, 4)


draw((0, 255, 0), False, spline_seg((100, -75), (400, 0), (445, -50), (0, 400)))  # L1 to cargo ship 2
draw((0, 0, 255), False, spline_seg((445, -50), (0, -50), (475, -200), (100, -200)))  # cargo ship 2 to pt
draw((0, 255, 255), False, spline_seg((475, -200), (-200, 400), (20, -210), (-200, 0)))  # pt to loading station
draw((255, 0, 0), False, spline_seg((20, -210), (200, 0), (210, -60), (0, 250)))  # loading station to pt
draw((255, 255, 0), False, spline_seg((210, -60), (0, -250), (330, -220), (120, -80)))  # pt to left rocket

draw((255, 0, 255), True, spline_seg((20, -210), (200, 0), (330, -220), (120, -80))) # dotted --
draw((255, 255, 255), True, spline_seg((445, -50), (0, -400), (20, -210), (-200, 0))) # dotted

# CENTER

draw((0, 255, 128), True, spline_seg((100, 0), (100, 0), (330, -18), (100, 0)))
draw((0, 128, 255), False, spline_seg((100, 0), (100, 0), (330, 18), (100, 0)))

#RIGHT

draw((255, 128, 0), False, spline_seg((100, 75), (200, 0), (390, 220), (-700, 400))) # far rocket
draw((255, 0, 128), True, spline_seg((390, 220), (175, -100), (445, 50), (0, -200))) # far rocket to cargo ship

draw((128, 0, 255), False, spline_seg((100, 75), (200, 0), (360, 200), (0, 400))) # mid rocket
draw((255, 0, 128), False, spline_seg((100, 75), (400, 0), (330, 220), (240, 160))) # near rocket

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if changed:
        changed = False
        pygame.display.flip()
