from colorsys import hsv_to_rgb, rgb_to_hsv
import random


def rainbow_spectrum(N):
    # create N hue, saturation, value tuples
    HSV = []
    for i in range(N):
        HSV.append((i/N, 1, 1))  # changing only the hue creates a spectrum

    # convert HSV to RGB
    unit_RGB = []
    for color in HSV:
        unit_RGB.append(hsv_to_rgb(color[0], color[1], color[2]))

    # convert the 0-1 valued unit_RGBs to RGBs from 0-255
    RGB = []
    for color in unit_RGB:
        RGB.append([color[0] * 255, color[1] * 255, color[2] * 255])

    return RGB


def generate_spectrum(N, start, end):
    start = rgb_to_hsv(start[0], start[1], start[2])
    end = rgb_to_hsv(end[0], end[1], end[2])

    # calculate the difference between the two HSV
    hue_diff = start[0] - end[0]
    saturation_diff = start[1] - end[1]
    value_diff = start[2] - end[2]

    HSV = []
    for i in range(N):
        HSV.append((start[0] - i * hue_diff / N, start[1] - i * saturation_diff / N, start[2] - i * value_diff / N))

    # convert HSV to RGB
    RGB = []
    for color in HSV:
        RGB.append(hsv_to_rgb(color[0], color[1], color[2]))

    RGB.reverse()
    return RGB


blue_theme = {
    "SCREEN": (6, 65, 76),
    "WINDOW": (23, 89, 101),

    "BORDER": (0, 0, 0),
    "CHESS_BOARD": (190, 183, 223),

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

    "BORDER": (15, 7, 24),
    "CHESS_BOARD": (151, 104, 209),

    "MAXIMISER": (0, 0, 0),
    "MINIMISER": (255, 255, 255),

    "TEXT_OUTPUT":  (143, 0, 255),

    "BUTTON": (0, 103, 166),
    "HOVERED": (151, 104, 209),

    "TEXT": (255, 255, 255),
    "RESET": (255, 0, 0)
}

old_green_theme = {
    "SCREEN": (13, 26, 8),
    "WINDOW": (58, 120, 34),

    "BORDER": (6, 30, 4),
    "CHESS_BOARD": (19, 83, 23),

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
