from enum import Enum


class Direction(Enum):
    """
    Enumeration of possible directions between adjacent cells in the maze.
    """
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


class Cell():
    """
    Represents a single cell in the maze grid.

    Each cell stores its grid position, wall states,
    and traversal metadata used during maze generation
    and solving.

    Attributes:
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        walls (dict[Direction, bool]): Mapping of wall presence
            for each direction. True means the wall exists.
        visited (bool): Indicates whether the cell has been visited.
        is42 (bool): Custom marker flag used by the application.
    """
    def __init__(self, row: int, col: int) -> None:
        """
        Initialize a cell with all walls enabled
        and an unvisited state.

        Args:
            row (int): Row position in the grid.
            col (int): Column position in the grid.
        """
        self.row = row
        self.col = col
        self.walls = {
            Direction.TOP: True,
            Direction.RIGHT: True,
            Direction.BOTTOM: True,
            Direction.LEFT: True
        }
        self.visited = False
        self.is42 = False

    def get_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
        """
        Return all orthogonally adjacent cells.

        Neighbors are collected only if they exist inside
        the grid boundaries.

        Args:
            matrix (list[list[Cell]]): Maze grid.

        Returns:
            list[Cell]: Adjacent neighboring cells.
        """
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
        """
        Return adjacent neighbors that have not been visited.

        Args:
            matrix (list[list[Cell]]): Maze grid.

        Returns:
            list[Cell]: Unvisited neighboring cells.
        """
        neighbors = self.get_neighbors(matrix)
        unvisited_neighbors = [n for n in neighbors if not n.visited]
        return unvisited_neighbors

    def get_valid_neighbors(self, matrix: list[list["Cell"]]) -> list["Cell"]:
        """
        Return reachable neighboring cells.

        A neighbor is considered reachable if there is no wall
        blocking movement from the current cell toward it.

        Args:
            matrix (list[list[Cell]]): Maze grid.

        Returns:
            list[Cell]: Connected neighboring cells.
        """
        valid = []
        neighbors = self.get_neighbors(matrix)
        for n in neighbors:
            direction = self.get_direction(n)
            if not self.walls[direction]:
                valid.append(n)
        return valid

    def remove_wall(self, direction: Direction) -> None:
        """
        Remove the wall in the specified direction.

        Args:
            direction (Direction): Wall direction to remove.
        """
        self.walls[direction] = False

    def get_direction(self, next_cell: "Cell") -> Direction:
        """
        Determine the relative direction of another cell.

        Both cells must share either the same row or the same column.

        Args:
            next_cell (Cell): Target cell.

        Returns:
            Direction: Direction from the current cell
            toward the target cell.

        Raises:
            MazeError: If the cells are not aligned
                horizontally or vertically.
        """
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
        """
        Create a passage between two adjacent cells
        by removing the corresponding walls.

        Args:
            cell2 (Cell): Cell to connect with.
        """
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

    def is_connected(self, cell2: "Cell") -> bool:
        """
        Check whether two adjacent cells are connected.

        Args:
            cell2 (Cell): Neighboring cell to evaluate.

        Returns:
            bool: True if there is no wall between the cells,
            False otherwise.
        """
        direction = self.get_direction(cell2)
        return not self.walls[direction]
