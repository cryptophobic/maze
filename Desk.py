import random
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple, Dict


class Directions(IntEnum):
    IDLE = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8
    ALL = 15

opposits = {Directions.UP: Directions.DOWN, Directions.DOWN: Directions.UP, Directions.LEFT: Directions.RIGHT, Directions.RIGHT: Directions.LEFT}
movements: Dict[Directions, Tuple[int, int]] = {Directions.IDLE: (0, 0), Directions.UP: (0, -1), Directions.RIGHT: (1, 0), Directions.DOWN: (0, 1), Directions.LEFT: (-1, 0)}

@dataclass
class Cell:
    ways: int = 0
    fixed: bool = False

class Desk:

    desk: List[List[Cell|None]]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.predefined: List[Tuple[int, int]] = []
        self.init_desk()

    def __getitem__(self, item):
        return self.desk[item]

    def init_desk(self):
        self.desk = [[Cell() for _ in range(self.height)] for _ in range(self.width)]
        # width_rooms = self.width // 9
        # width_rooms = 3 if width_rooms > 3 else width_rooms
        # room_width = 0
        # if width_rooms > 0:
        #     room_width_place = self.width // width_rooms
        #     room_width = room_width_place // 3
        #
        # height_rooms = self.height // 9
        # height_rooms = 3 if height_rooms > 3 else height_rooms
        # room_height = 0
        # if width_rooms > 0:
        #     room_height_place = self.height // height_rooms
        #     room_height = room_height_place // 3
        #
        # for w in range(width_rooms):
        #     for h in range(height_rooms):
        #         for x in range(room_width):
        #             for y in range(room_height):
        #                 hor = x + room_width * 2 *(w + 1)
        #                 vert = y + room_height * 2 * (h + 1)
        #                 ways = Directions.ALL
        #                 if x == 0:
        #                     ways -= Directions.LEFT
        #                 if y == 0:
        #                     ways -= Directions.UP
        #
        #
        #                 if x == room_width - 1:
        #                     ways -= Directions.RIGHT
        #                 if y == room_height - 1:
        #                     ways -= Directions.DOWN
        #                 self.desk[hor][vert].ways = ways
        #                 if x == 0 and y == 1:
        #                     self.desk[hor][vert].ways = Directions.IDLE
        #                     # self.predefined.append((hor, vert))
        #                 else:
        #                     self.desk[hor][vert].fixed = True


    def move(self, x: int, y: int, direction: Directions = Directions.IDLE) -> Tuple[int, int]:
        return x + movements[direction][0], y + movements[direction][1]

    def is_empty(self, x: int, y: int, direction: Directions = Directions.IDLE) -> bool:
        (x, y) = self.move(x, y, direction)
        res = self.width > x >= 0 and 0 <= y < self.height
        return res and 0 == self.desk[x][y].ways

    def move_rand(self, x, y) -> Tuple[int, int] | None:
        directions = [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]
        directions = list(filter(lambda i: (self.desk[x][y].ways & int(i) == 0), directions))

        while len(directions) > 0:
            direction = random.choice(directions)
            if self.is_empty(x, y, direction):
                self.desk[x][y].ways |= direction
                (x, y) = self.move(x, y, direction)
                self.desk[x][y].ways |= opposits[direction]
                return x, y

            directions.remove(direction)

        self.desk[x][y].fixed = True
        return None

