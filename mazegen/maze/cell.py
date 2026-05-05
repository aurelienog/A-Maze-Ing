from enum import Enum


class Direction(Enum):
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

    def get_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
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

    def get_valid_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
        valid = []
        neighbors = self.get_unvisited_neighbors(matrix)
        for n in neighbors:
            direction = self.get_direction(n)
            if not self.walls[direction]:
                valid.append(n)
        return valid

    def remove_wall(self, direction: Direction) -> None:
        self.walls[direction] = False

    def get_direction(self, next_cell: "Cell") -> Direction:
        from .maze import MazeError
        if self.col == next_cell.col:
            if self.row > next_cell.row:
                return Direction.TOP
            else:
                return Direction.BOTTOM
        elif self.row == next_cell.row:
            if self.col > next_cell.col:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        else:
            raise MazeError(f"Cells are not neighbors: {self} - {next_cell}")

    def connect_cells(self, cell2: "Cell") -> None:
        direction = self.get_direction(cell2)
        match direction:
            case Direction.TOP:
                self.remove_wall(Direction.TOP)
                cell2.remove_wall(Direction.BOTTOM)
            case Direction.RIGHT:
                self.remove_wall(Direction.RIGHT)
                cell2.remove_wall(Direction.LEFT)
            case Direction.BOTTOM:
                self.remove_wall(Direction.BOTTOM)
                cell2.remove_wall(Direction.TOP)
            case Direction.LEFT:
                self.remove_wall(Direction.LEFT)
                cell2.remove_wall(Direction.RIGHT)
