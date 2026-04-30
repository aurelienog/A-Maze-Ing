from .maze import Maze
from .cell import Cell


class MazeGenerator():
    def __init__(self, seed=None) -> None:
        self.seed = seed

    def generate_DFS_maze(self, width, height):
        """
        Generate and show a maze, using the simple Depth-first search algorithm.

        Start at a random cell.
        Mark the current cell as visited, and get a list of its neighbors. For each
        neighbor, starting with a randomly selected neighbor:

        If that neighbor hasn't been visited, remove the wall between this cell and
        that neighbor, and then recurse with that neighbor as the current cell.
        """

        if self.seed is not None:
            ...
        else:
            ...
        return Maze(...)
