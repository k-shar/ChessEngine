from math import e
from random import randint
import matplotlib.pyplot as plt
from engine_config import piece_values
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


def normalise_evaluation(eval):
    scale = 0.4
    tanhx = ((e**(scale * eval) - 1)/(e**(scale * eval) + 1))
    return (tanhx + 1) / 2


def generate_evaluation_spectrum(start, end):
    spectrum = []
    N = 50
    for i in range(N):
        spectrum.append(start + (end-start)*i/N)
    spectrum.reverse()
    return spectrum


def static_evaluation(piece_group):
    evaluation = 0
    polarity = 0

    for piece in piece_group:
        if piece.color == "white":
            polarity = -1
        if piece.color == "black":
            polarity = 1

        if type(piece) is Pawn:
            evaluation += polarity * piece_values["pawn"]
        if type(piece) is Rook:
            evaluation += polarity * piece_values["rook"]
        if type(piece) is Knight:
            evaluation += polarity * piece_values["knight"]
        if type(piece) is Bishop:
            evaluation += polarity * piece_values["bishop"]
        if type(piece) is Queen:
            evaluation += polarity * piece_values["queen"]

    return round(evaluation, 4)


if __name__ == "__main__":
    infinity = 15

    input_evaluations = []
    for i in range(100):
        input_evaluations.append(randint(-infinity, infinity))

    evaluation_slider_center = []
    for input in input_evaluations:
        print(input)
        evaluation_slider_center.append(normalise_evaluation(input))

    plt.plot(input_evaluations, evaluation_slider_center, "x")
    plt.show()

    print(generate_evaluation_spectrum(5, 50))