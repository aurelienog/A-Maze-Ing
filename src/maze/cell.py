from enum import Enum


class Direction(str, Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


class Cell():
    def __init__(self) -> None:
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
        self.visited = False

    def remove_wall(self, direction: Direction) -> None:
        self.walls[direction] = False
