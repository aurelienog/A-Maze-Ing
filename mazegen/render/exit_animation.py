import os
import random
import time

ASCII_BLOCK = "█"
DEFAULT_GAP = 2
DEFAULT_SCALE = 2


def clear() -> None:
    """
    Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


LETTER_E = [
    "█████",
    "█    ",
    "█    ",
    "████ ",
    "█    ",
    "█    ",
    "█████",
]

LETTER_X = [
    "█   █",
    " █ █ ",
    "  █  ",
    "  █  ",
    "  █  ",
    " █ █ ",
    "█   █",
]

LETTER_I = [
    " ███ ",
    "  █  ",
    "  █  ",
    "  █  ",
    "  █  ",
    "  █  ",
    " ███ ",
]

LETTER_T = [
    "█████",
    "  █  ",
    "  █  ",
    "  █  ",
    "  █  ",
    "  █  ",
    "  █  ",
]


def compose_word(*letters: list[str], gap: int = DEFAULT_GAP) -> list[str]:
    """
    Combine ASCII-art letters into a single word.

    Args:
        *letters (list[str]):
            ASCII-art letter definitions.
        gap (int):
            Horizontal spacing between letters.

    Returns:
        list[str]:
            Combined ASCII-art lines.
    """
    if not letters:
        return []

    spacer = " " * gap

    return [
        spacer.join(letter[row] for letter in letters)
        for row in range(len(letters[0]))
    ]


def scale_horizontal(lines: list[str], factor: int = DEFAULT_SCALE) -> list[str]:
    """
    Scale ASCII-art horizontally.

    Args:
        lines (list[str]):
            ASCII-art lines.
        factor (int):
            Horizontal scaling factor.

    Returns:
        list[str]:
            Scaled ASCII-art.
    """
    return [
        "".join(ch * factor for ch in line)
        for line in lines
    ]


def make_frames(
    base_lines: list[str],
    max_frames: int = 45,
    seed: int = 42
) -> list[str]:
    """
    Generate animation frames by progressively removing blocks.

    Args:
        base_lines (list[str]):
            Initial ASCII-art image.
        max_frames (int):
            Approximate number of animation frames.
        seed (int):
            Random seed controlling removal order.

    Returns:
        list[str]:
            Animation frames.
    """
    positions: list[tuple[int, int]] = []

    for y, line in enumerate(base_lines):
        for x, ch in enumerate(line):
            if ch == ASCII_BLOCK:
                positions.append((y, x))

    rnd = random.Random(seed)
    rnd.shuffle(positions)

    total = len(positions)
    step = max(1, total // (max_frames - 2))

    frames: list[str] = []

    for k in range(0, total + 1, step):
        canvas = [list(line) for line in base_lines]

        for i in range(k):
            y, x = positions[i]
            canvas[y][x] = " "

        frames.append(
            "\n".join("".join(row) for row in canvas)
        )

    empty = "\n".join(
        "".join(" " if ch == ASCII_BLOCK else ch for ch in row)
        for row in base_lines
    )

    flash = "\n".join(
        "".join("." if ch == ASCII_BLOCK else ch for ch in row)
        for row in base_lines
    )

    frames.append(empty)
    frames.append(flash)

    return frames


def animate_exit(delay: float = 0.04) -> None:
    """
    Render and animate the EXIT ASCII-art effect.

    Args:
        delay (float):
            Delay between animation frames in seconds.
    """
    base = compose_word(
        LETTER_E,
        LETTER_X,
        LETTER_I,
        LETTER_T,
    )

    base_scaled = scale_horizontal(base)

    frames = make_frames(
        base_scaled,
        max_frames=48,
        seed=int(time.time()) & 0xFFFF
    )

    for frame in frames:
        clear()
        print("\n" + frame + "\n")
        time.sleep(delay)

    clear()


if __name__ == "__main__":
    animate_exit(delay=0.05)
