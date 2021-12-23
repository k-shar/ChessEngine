# config
RAINBOW_MOUSE = True
MOUSE_TRAIL = False
RAINBOW_COLOR_SPECTRUM_SIZE = 300
FADE_DURATION = 15

""" color themes """
blue_theme = {
    "SCREEN": (6, 65, 76),
    "WINDOW": (23, 89, 101),

    "LEGAL_MOVE": (0, 0, 255),

    "WHITE": (179, 179, 179),
    "BLACK": (88, 88, 88),

    "BORDER": (0, 0, 0),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (255, 255, 255),

    "TEXT_OUTPUT": (80, 175, 223),

    "BUTTON": (162, 163, 187),
    "HOVERED": (100, 100, 255),

    "TEXT": (255, 255, 255),
    "RESET": (255, 0, 0)
}

purple_theme = {
    "SCREEN": (37, 6, 76),
    "WINDOW": (85, 50, 133),

    "LEGAL_MOVE": (255, 0, 255),

    "WHITE": (235, 235, 235),
    "BLACK": (139, 116, 180),

    "BORDER": (0, 0, 0),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (255, 255, 255),

    "TEXT_OUTPUT": (143, 0, 255),

    "BUTTON": (0, 103, 166),
    "HOVERED": (150, 237, 137),

    "TEXT": (255, 255, 255),
    "RESET": (255, 0, 0)
}

green_theme = {
    "SCREEN": (13, 26, 8),
    "WINDOW": (0, 40, 0),

    "LEGAL_MOVE": (0, 255, 0),

    "WHITE": (232, 234, 229),
    "BLACK": (51, 105, 75),

    "BORDER": (0, 0, 0),

    "MAXIMISER": (231, 118, 106),
    "MINIMISER": (80, 175, 101),

    "TEXT_OUTPUT": (21, 16, 240),

    "BUTTON": (0, 103, 166),
    "HOVERED": (44, 29, 255),

    "TEXT": (255, 255, 255),
    "RESET": (255, 0, 0)
}

all_black = {
    "SCREEN": (0, 0, 0),
    "WINDOW": (0, 0, 0),

    "WHITE": (0, 0, 0),
    "BLACK": (0, 0, 0),

    "BORDER": (0, 0, 0),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (0, 0, 0),

    "TEXT_OUTPUT": (0, 0, 0),

    "BUTTON": (0, 0, 0),
    "HOVERED": (0, 0, 0),

    "TEXT": (0, 0, 0),
    "RESET": (0, 0, 0)
}

default_theme = blue_theme.copy()

random_theme = all_black.copy()
random_theme["WINDOW"] = (1, 2, 3)
