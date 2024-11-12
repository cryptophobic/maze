import random
from collections import deque
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
    passing: bool = False

class Desk:

    desk: List[List[Cell|None]]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.predefined: List[Tuple[int, int]] = []
        self.init_desk()

    def __getitem__(self, item):
        return self.desk[item]

    def solution(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]] | None:
        queue = deque([(start, [start])])  # store path to trace the solution
        visited = {start}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
                # for (x, y) in path:
                #     self.desk[x][y].passing = True
                return path # Return path from start to end

            for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
                res = self.is_can_move(x, y, direction)
                (nx, ny) = self.move(x, y, direction)

                if res and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

        return None

    def init_desk(self):
        self.desk = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

    def move(self, x: int, y: int, direction: Directions = Directions.IDLE) -> Tuple[int, int]:
        return x + movements[direction][0], y + movements[direction][1]

    def is_empty(self, x: int, y: int, direction: Directions = Directions.IDLE) -> bool:
        (x, y) = self.move(x, y, direction)
        res = self.width > x >= 0 and 0 <= y < self.height
        return res and 0 == self.desk[x][y].ways

    def is_can_move(self, x: int, y: int, direction: Directions = Directions.IDLE) -> bool:
        (nx, ny) = self.move(x, y, direction)
        res = self.width > nx >= 0 and 0 <= ny < self.height
        return res and self.desk[x][y].ways & direction == direction

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

