from enum import Enum


class Direction(str, Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


class Cell():
    def __init__(self, row: int, col: int, matrix: list[list["Cell"]]) -> None:
        self.row = row
        self.col = col
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
        self.visited = False

    def get_neighbors(self, matrix) -> list["Cell"]:
        neighbors = []
        if self.col > 0:
            left_neighbor = matrix[self.row][self.col - 1]
            neighbors.append(left_neighbor)
            
        if self.col < len(matrix[0]) - 1:
            right_neighbor = matrix[self.row][self.col + 1]
            neighbors.append(right_neighbor)

        if self.row > 0:
            top_neighbor = matrix[self.row - 1][self.col]
            neighbors.append(top_neighbor)

        if self.row < len(matrix) - 1:
            bottom_neighbor = matrix[self.row + 1][self.col]
            neighbors.append(bottom_neighbor)
        return neighbors

    def get_unvisited_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
        neighbors = self.get_neighbors(matrix)
        unvisited_neighbors = [n for n in neighbors if not n.visited]
        return unvisited_neighbors

    def remove_wall(self, direction: Direction) -> None:
        self.walls[direction] = False

    def __repr__(self):
        return "[X]"