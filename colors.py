from colorsys import hsv_to_rgb, rgb_to_hsv


def rainbow_spectrum(N):
    # create N hue, saturation, value tuples
    HSV = []
    for i in range(N):
        HSV.append((i / N, 1, 1))  # changing only the hue creates a spectrum

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
