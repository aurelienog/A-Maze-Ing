from enum import Enum


class Direction(str, Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


class Cell():
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
        self.visited = False

    def remove_wall(self, direction: Direction) -> None:
        self.walls[direction] = False

    def __repr__(self):
        return "[X]"