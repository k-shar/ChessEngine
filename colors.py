from colorsys import hsv_to_rgb
import seaborn


def generate_color_spectrum(N):
    # create N hue, saturation, value tuples
    HSV = []
    for i in range(N):
        HSV.append((i/N, 1, 1))  # changing only the hue creates a spectrum

    # convert HSV to RGB using the hsv_to_rgb from colorsys
    unit_RGB = []
    for color in HSV:
        unit_RGB.append(hsv_to_rgb(color[0], color[1], color[2]))

    # convert the 0-1 valued unit_RGBs to RGBs from 0-255
    RGB = []
    for color in unit_RGB:
        RGB.append([color[0] * 255, color[1] * 255, color[2] * 255])

    return RGB
