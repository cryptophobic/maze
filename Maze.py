import random
from enum import Enum
from typing import List, Tuple

from Desk import Desk

class Choice(Enum):
    nothing = 0,
    newest = 1,
    oldest = 2,
    random = 3,

class Maze:
    def __init__(self, desk: Desk):
        self.dead_end = False
        self.on_dead_end: Choice = Choice.nothing
        self.choices = [(750, Choice.newest), (10000, Choice.random)]
        self.desk = desk
        self.cells: List[Tuple[int, int]] = [(0, 0)]

    def __random_cell(self) -> Tuple[int, int]:
        return random.choice(self.cells)

    def __newest_cell(self) -> Tuple[int, int]:
        return self.cells[-1]

    def __oldest_cell(self) -> Tuple[int, int]:
        return self.cells[0]

    def __produce_cell(self, choice: Choice) -> Tuple[int, int]:
        match choice:
            case Choice.newest:
                return self.__newest_cell()
            case Choice.oldest:
                return self.__oldest_cell()
            case Choice.random:
                return self.__random_cell()

    def process_next_cell(self):
        if not self.cells:
            return

        cell = None
        if self.dead_end and self.on_dead_end != Choice.nothing:
            cell = self.__produce_cell(self.on_dead_end)
        elif len(self.choices) > 0:
            pick = random.choice(range(1000))
            for choice in self.choices:
                if pick < choice[0]:
                    cell = self.__produce_cell(choice[1])
                    break

        cell = self.__newest_cell() if cell is None else cell

        new_cell = self.desk.move_rand(cell[0], cell[1])
        if new_cell is None:
            self.cells.remove(cell)
            self.dead_end = True
        else:
            self.cells.append(new_cell)
            self.dead_end = False

