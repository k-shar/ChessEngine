from colorsys import hsv_to_rgb
import seaborn


def generate_color_spectrum(N):
    # create N hue, saturation, value tuples
    HSV = []
    for i in range(N):
        HSV.append((i / N, 1, 1))  # changing only the hue creates a spectrum

    # convert HSV to RGB using the hsv_to_rgb from colorsys
    unit_RGB = []
    for color in HSV:
        unit_RGB.append(hsv_to_rgb(color[0], color[1], color[2]))

    # convert the 0-1 valued unit_RGBs to RGBs from 0-255
    RGB = []
    for color in unit_RGB:
        RGB.append([color[0] * 255, color[1] * 255, color[2] * 255])

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

green_theme = {
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

default_theme = blue_theme
