from .cell import Cell

class Maze():
    def __init__(self, matrix, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.matrix = matrix
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        
        def display(self) -> None:
            for row in self.matrix:
                print(" ".join(str(cell) for cell in row))
