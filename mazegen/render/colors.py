
class ColorPalette:
    RESET = "\033[0m"

    # foreground
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    GRAY = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"

    # background
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    BG_LIGHT_RED = "\033[101m"
    BG_LIGHT_GREEN = "\033[102m"
    BG_LIGHT_YELLOW = "\033[103m"
    BG_LIGHT_BLUE = "\033[104m"
    BG_LIGHT_MAGENTA = "\033[105m"
    BG_LIGHT_CYAN = "\033[106m"

    COLORS = [
        RED,
        GREEN,
        YELLOW,
        BLUE,
        MAGENTA,
        CYAN,
        WHITE,
        GRAY,
        LIGHT_RED,
        LIGHT_GREEN,
        LIGHT_YELLOW,
        LIGHT_BLUE,
        LIGHT_MAGENTA,
        LIGHT_CYAN
        ]

    BACKGROUNDS = [
            BG_GREEN,
            BG_YELLOW,
            BG_BLUE,
            BG_MAGENTA,
            BG_CYAN,
            BG_WHITE,
            BG_RED,
            BG_LIGHT_RED,
            BG_LIGHT_GREEN,
            BG_LIGHT_YELLOW,
            BG_LIGHT_BLUE,
            BG_LIGHT_MAGENTA,
            BG_LIGHT_CYAN,
        ]

    def __init__(self) -> None:
        self.index = 0
        self.entry = self.COLORS[self.index % 14]
        self.exit = self.COLORS[(self.index + 1) % 14]
        self.path_color = self.COLORS[(self.index + 2) % 14]
        self.is42 = self.BACKGROUNDS[self.index % 13]
        self.walls = self.COLORS[self.index + 6 % 14]

    def choose_next_color(self) -> None:
        self.index += 1
        self.entry = self.COLORS[self.index % 14]
        self.exit = self.COLORS[(self.index + 1) % 14]
        self.path_color = self.COLORS[(self.index + 2) % 14]
        self.is42 = self.BACKGROUNDS[self.index % 13]
        self.walls = self.COLORS[(self.index + 6) % 14]
