from ..maze import MazeGenerator, Maze


def create_fixed_maze() -> Maze:
    entry = (0, 0)
    end = (19, 14)

    generator = MazeGenerator()

    maze = generator.generate_perfect_maze(
        20,
        20,
        entry,
        end,
    )

    return maze
