from .maze import Maze
from .cell import Cell, Direction
from random import random

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
        matrix: list[list[Cell]] = [[Cell(row, col) for col in range(width)] for row in range(height)]

        line = random.choice(matrix)
        current_cell = random.choice(line)
        current_cell.visited = True

        neighbors = current_cell.get_unvisited_neighbors(matrix)

        if len(neighbors) > 0:
            next_cell = random.choice(neighbors)

        next_cell_position = 
        match next_cell_position:
        
            case Direction.BOTTOM: 
                current_cell.remove_wall(current_cell[Direction.TOP])
                next_cell.remove_wall(current_cell[Direction.BOTTOM])
            case Direction.LEFT:
                current_cell.remove_wall(current_cell[Direction.RIGHT])
                next_cell.remove_wall(current_cell[Direction.LEFT])
            case Direction.TOP:
                current_cell.remove_wall(current_cell[Direction.BOTTOM])
                next_cell.remove_wall(current_cell[Direction.TOP])
            case Direction.RIGHT:
                current_cell.remove_wall(current_cell[Direction.LEFT])
                next_cell.remove_wall(current_cell[Direction.RIGHT])
        
        # if self.seed is not None:
        #     ...
        # else:
        #     ...
        return Maze(...)
