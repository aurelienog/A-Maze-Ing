import os
import time
import random


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


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


def compose_word(*letters: list[str], gap: int = 2) -> list[str]:
    lines = []
    spacer = " " * gap
    for row in range(len(letters[0])):
        lines.append(spacer.join(letter[row] for letter in letters))
    return lines


def scale_horizontal(lines: list[str], factor: int = 2) -> list[str]:
    scaled = []
    for line in lines:
        new_line = []
        for ch in line:
            new_line.append(ch * factor)
        scaled.append("".join(new_line))
    return scaled


def make_frames(base_lines: list[str],
                max_frames: int = 45,
                seed: int = 42) -> list[str]:
    positions = []
    for y, line in enumerate(base_lines):
        for x, ch in enumerate(line):
            if ch == "█":
                positions.append((y, x))

    rnd = random.Random(seed)
    rnd.shuffle(positions)

    frames = []
    total = len(positions)
    step = max(1, total // (max_frames - 2))
    for k in range(0, total + 1, step):
        canvas = [list(line) for line in base_lines]
        for i in range(k):
            y, x = positions[i]
            canvas[y][x] = " "
        frames.append("\n".join("".join(row) for row in canvas))

    empty = "\n".join("".join(' ' if ch == '█' else ch for ch in row)
                      for row in base_lines)
    flash = "\n".join("".join('.' if ch == '█' else ch for ch in row)
                      for row in base_lines)
    frames.append(empty)
    frames.append(flash)
    return frames


def exit_animation(delay: float = 0.04) -> None:
    base = compose_word(LETTER_E, LETTER_X, LETTER_I, LETTER_T, gap=2)
    base_scaled = scale_horizontal(base, factor=2)

    frames = make_frames(base_scaled, max_frames=48, seed=int(time.time()) & 0xFFFF)
    for frame in frames:
        clear()
        print("\n" + frame + "\n")
        time.sleep(delay)
    clear()


if __name__ == "__main__":
    exit_animation(delay=0.05)
