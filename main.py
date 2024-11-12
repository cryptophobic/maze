import random
import time
from dataclasses import dataclass
from typing import List, Tuple
import operator

import pygame
from pygame.mixer_music import queue

from Desk import Desk
from Maze import Maze, Choice
from Render import Render


def passkey():
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

if __name__ == "__main__":
    HEIGHT = 49
    WIDTH = 74
    # HEIGHT = 20
    # WIDTH = 20
    # HEIGHT = int(49 * 6.5)
    # WIDTH = int(74 * 6.5)

    start = (WIDTH // 2, HEIGHT // 2)
    # start = (0, 0)

    renderer = Render(20, (10, 10))
    desk = Desk(WIDTH, HEIGHT)
    maze = Maze(desk)

    variants = [
        [
            'Recursive Backtracking',
            Choice.nothing,
            [(10000, Choice.newest)]
        ],
        [
            'Prim',
            Choice.nothing,
            [(10000, Choice.random)]
        ],
        [
            '75/25 newest-random',
            Choice.nothing,
            [(750, Choice.newest), (10000, Choice.random)]
        ],
        [
            '25/75 newest-random',
            Choice.nothing,
            [(750, Choice.random), (10000, Choice.newest)]
        ],
        [
            'deadend-oldest',
            Choice.oldest,
            [(10000, Choice.newest)]
        ],
        [
            'deadend-random',
            Choice.random,
            [(10000, Choice.newest)]
        ],
        [
            'oldest',
            Choice.nothing,
            [(10000, Choice.oldest)]
        ]

    ]

    processed = 0
    generated = 0
    while not check_exit():
        processed += 1
        maze.process_next_cell()
        if processed > 10:
            processed = 0
            renderer.draw(desk)

        if passkey() or len(maze.cells) == 0:
            path = desk.solution((0, 0), (WIDTH - 1, HEIGHT - 1))
            for (x, y) in path:
                desk[x][y].fixed = False
                renderer.draw(desk)

            for (x, y) in path:
                desk[x][y].fixed = True
                desk[x][y].passing = True

            renderer.draw(desk)
            time.sleep(2)
            desk = Desk(WIDTH, HEIGHT)
            maze = Maze(desk)
            variant = variants[generated % len(variants)]
            generated += 1
            print(variant[0])
            maze.on_dead_end = variant[1]
            maze.choices = variant[2]

    renderer.quit()
