RAINBOW_MOUSE = False

""" color themes """
blue_theme = {
    "SCREEN": (6, 65, 76),
    "WINDOW": (23, 89, 101),

    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),

    "BORDER": (0, 0, 0),
    "CHESS_BOARD": (0, 0, 0),

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

    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),

    "BORDER": (0, 0, 0),
    "CHESS_BOARD": (0, 0, 0),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (255, 255, 255),

    "TEXT_OUTPUT": (143, 0, 255),

    "BUTTON": (0, 103, 166),
    "HOVERED": (151, 104, 209),

    "TEXT": (255, 255, 255),
    "RESET": (255, 0, 0)
}

old_green_theme = {
    "SCREEN": (13, 26, 8),
    "WINDOW": (58, 120, 34),

    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),

    "BORDER": (0, 0, 0),
    "CHESS_BOARD": (0, 0, 0),

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
    "CHESS_BOARD": (0, 0, 0),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (0, 0, 0),

    "TEXT_OUTPUT": (0, 0, 0),

    "BUTTON": (0, 0, 0),
    "HOVERED": (0, 0, 0),

    "TEXT": (0, 0, 0),
    "RESET": (0, 0, 0)
}

default_theme = blue_theme.copy()
multi_theme = all_black.copy()

random_theme = all_black.copy()
random_theme["WINDOW"] = (1, 2, 3)
