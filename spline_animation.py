import sys
import time

import pygame

from generated_data import trajectory

SIZE = W, H = (495, 493)
pygame.init()
display = pygame.display.set_mode(SIZE)
changed = True

display.fill((255, 255, 255))

img = pygame.image.load("field.PNG")
display.blit(img, (0, 0))

clock = pygame.time.Clock()

start_time = time.time()
last_time = start_time

i = 0

def tx(ox):
    return int(247 - ox)


def ty(oy):
    return int(493 - oy)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    new_time = time.time()
    dt = new_time - last_time
    last_time = new_time
    elapsed = new_time - start_time
    while i < len(trajectory) - 2 and trajectory[i][0] < elapsed:
        i += 1
    if i == len(trajectory) - 2:
        continue
    moment_0 = trajectory[i]
    moment_1 = trajectory[i + 1]
    x = (elapsed - moment_0[0]) / (moment_1[0] - moment_0[0])
    px = moment_0[1] + (moment_1[1] - moment_0[1]) * x
    py = moment_0[2] + (moment_1[2] - moment_0[2]) * x
    pygame.draw.circle(display, (0,255,0), (tx(py * 18), ty(px * 18)), 2)
    pygame.display.flip()
    clock.tick(50)
