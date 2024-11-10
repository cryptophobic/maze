import random

import pygame

from Desk import Desk


class Render:
    def __init__(self, width, offset):
        pygame.init()
        self.width = width
        self.offset = offset
        self.screen = pygame.display.set_mode((1500, 1000), 0, 32)
        pygame.display.set_caption("Hello Maze")
        self.screen.fill((0, 0, 0))

    def draw(self, desk: Desk):
        self.screen.fill((0, 0, 0))
        for x in range(len(desk.desk)):
            for y in range(len(desk.desk[x])):
                top_left = (x * self.width + self.offset[0], y * self.width + self.offset[1])
                top_right = (x * self.width + self.offset[0] + self.width, y * self.width + self.offset[1])
                bottom_left = (x * self.width + self.offset[0], y * self.width + self.offset[1] + self.width)
                bottom_right = (x * self.width + self.offset[0] + self.width, y * self.width + self.offset[1] + self.width)
                blue_effect = 60 if random.choice(range(10)) > 4 else 50
                color = (30, 30, blue_effect) if desk[x][y].ways == 0 else (255, 255, 255)
                brick_color = (0, 0, 0) if desk[x][y].fixed else (100, 0, 0)
                brick_color = (30, 30, blue_effect) if desk[x][y].ways == 0 else brick_color

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
