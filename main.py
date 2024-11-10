import random
import time
from dataclasses import dataclass
from typing import List, Tuple
import operator

import pygame

pygame.init()
screen = pygame.display.set_mode((1500, 1000), 0, 32)
pygame.display.set_caption("Hello Maze")
screen.fill((0, 0, 0))
pygame.display.update()


def passkeye():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        # print("You pressed the space")
        return True
    return False


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        return True

    return False

width = 20
offset = (10, 10)

def draw():
    screen.fill((0, 0, 0))
    for x in range(len(desk)):
        for y in range(len(desk[x])):
            top_left = (x*width + offset[0], y*width + offset[1])
            top_right = (x*width + offset[0] + width, y*width + offset[1])
            bottom_left = (x*width + offset[0], y*width + offset[1] + width)
            bottom_right = (x*width + offset[0] + width, y*width + offset[1] + width)
            color = (30, 30, 60 if random.choice(range(10)) > 4 else 50) if desk[x][y].ways == 0 else (255, 255, 255)
            brick_color = (0, 0, 0) if desk[x][y].fixed else (100, 0, 0)
            brick_color = (30, 30, 60 if random.choice(range(10)) > 4 else 50) if desk[x][y].ways == 0 else brick_color

            pygame.draw.rect(screen, brick_color, pygame.Rect(top_left[0], top_left[1], width, width))


            if not desk[x][y].ways & UP:
                pygame.draw.line(screen, color, top_left, top_right, width=1)

            if not desk[x][y].ways & RIGHT:
                pygame.draw.line(screen, color, top_right, bottom_right, width=1)

            if not desk[x][y].ways & DOWN:
                pygame.draw.line(screen, color, bottom_right, bottom_left, width=1)

            if not desk[x][y].ways & LEFT:
                pygame.draw.line(screen, color, top_left, bottom_left, width=1)
    pygame.display.update()


@dataclass
class Cell:
    ways: int = 0
    fixed: bool = False

IDLE = 0
UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8

HEIGHT = 49
WIDTH = 74
# HEIGHT = 10
# WIDTH = 10


opposits = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
movements = {IDLE: (0, 0), UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)}

start = (WIDTH // 2, HEIGHT // 2)
# start = (0, 0)
def init_desk() -> List[List[Cell|None]]:
    return [[Cell() for y in range(HEIGHT)] for x in range(WIDTH)]

desk = init_desk()

def move(x: int, y: int, direction: int = IDLE) -> Tuple:
    return tuple(map(operator.add, (x, y), movements[direction]))

def is_empty(x: int, y: int, direction: int = IDLE) -> bool:
    (x, y) = move(x, y, direction)
    res = WIDTH > x >= 0 and 0 <= y < HEIGHT
    return res and 0 == desk[x][y].ways

def move_rand(x, y) -> tuple | None:
    directions = [UP, DOWN, LEFT, RIGHT]
    directions = list(filter(lambda i: (desk[x][y].ways & i == 0), directions))

    while len(directions) > 0:
        direction = random.choice(directions)
        if is_empty(x, y, direction):
            desk[x][y].ways |= direction
            (x, y) = move(x, y, direction)
            desk[x][y].ways |= opposits[direction]
            return x, y

        directions.remove(direction)

    desk[x][y].fixed = True
    return None

bang = True
cells = [start]
def process_next_cell(bang):
    choice = random.choice(range(1000))
    # if bang is True:
    #     cell = random.choice(cells)
    #     # cell = cells[0]
    # else:
    #     cell = cells[-1]

    if choice > -1:
        cell = cells[-1]
    else:
        cell = random.choice(cells)

    # print(cells)
    new_cell = move_rand(cell[0], cell[1])
    if new_cell is None:
        cells.remove(cell)
        return True
    else:
        cells.append(new_cell)
        return False

processed = 0
last_cell = start
while not check_exit():

    last_cell = cells[-1] if len(cells) > 0 else last_cell

    if len(cells) > 0:
        if True or passkeye():
            old_bang = bang
            bang = process_next_cell(bang)
            processed += 1
            choice = random.choice(range(1000))
            # if bang != old_bang:
            if processed > 100:
                processed = 0
                draw()
                # time.sleep(0.2)
            #time.sleep(0.03)
    else:
        draw()

    # if passkeye() or len(cells) == 0:
    if passkeye():
        desk = init_desk()
        cells = [(random.choice(range(WIDTH)), random.choice(range(HEIGHT)))]
        time.sleep(0.1)

# pygame.draw.rect(screen, (255, 100, 0), (10, 10, 80, 80))

pygame.quit()

