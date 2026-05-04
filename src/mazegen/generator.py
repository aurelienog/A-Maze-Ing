from .maze import Maze, MazeError
from .cell import Cell
import random


class MazeGenerator():
    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def generate_DFS_maze(self, width: int, height: int,
                          entry: tuple[int, int], exit: tuple[int, int]) -> Maze:
        """
        Generate and show a maze, using the simple Depth-first search algorithm.

        Start at a random cell.
        Mark the current cell as visited, and get a list of its neighbors. For each
        neighbor, starting with a randomly selected neighbor:

        If that neighbor hasn't been visited, remove the wall between this cell and
        that neighbor, and then recurse with that neighbor as the current cell.
        """
        matrix: list[list[Cell]] = [[Cell(row, col) for col in range(width)]
                                    for row in range(height)]
        entry_cell = None
        exit_cell = None
        for row in matrix:
            for cell in row:
                if (cell.row, cell.col) == entry:
                    entry_cell = cell
                elif (cell.row, cell.col) == exit:
                    exit_cell = cell
        if exit_cell is None or entry_cell is None:
            raise MazeError("Entry and exit are mandatory")

        line = self.rng.choice(matrix)
        current_cell = self.rng.choice(line)

        def build(current_cell: Cell) -> None:
            current_cell.visited = True
            unvisited_neighbors = current_cell.get_unvisited_neighbors(matrix)
            self.rng.shuffle(unvisited_neighbors)

            for neighbor in unvisited_neighbors:
                if not neighbor.visited:
                    next_cell = neighbor
                    current_cell.connect_cells(next_cell)
                    build(next_cell)

        build(current_cell)

        return Maze(matrix, width, height, entry_cell, exit_cell)
