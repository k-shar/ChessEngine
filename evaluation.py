from math import e
from random import randint
import matplotlib.pyplot as plt
from engine_config import piece_values
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from fen_manipulation import instasiate_pieces, make_move_on_FEN
from threading import Thread


def normalise_evaluation(eval):
    try:
        scale = 0.4
        tanhx = ((e**(scale * eval) - 1)/(e**(scale * eval) + 1))
        return (tanhx + 1) / 2
    except OverflowError:
        return 100

def generate_evaluation_spectrum(start, end):
    spectrum = []
    N = 50
    for i in range(N):
        spectrum.append(start + (end-start)*i/N)
    spectrum.reverse()
    return spectrum


def relative_piece_sum(piece_group):
    evaluation = 0
    # polarity to decide weather the piece adds or subtracts from the evaluation
    for piece in piece_group:
        if piece.color == "white":
            polarity = -1
        elif piece.color == "black":
            polarity = 1
        else:
            raise Exception(f"'{piece.color}' is not black or white")

        if type(piece) is Pawn:
            evaluation += polarity * piece_values["pawn"]
        elif type(piece) is Rook:
            evaluation += polarity * piece_values["rook"]
        elif type(piece) is Knight:
            evaluation += polarity * piece_values["knight"]
        elif type(piece) is Bishop:
            evaluation += polarity * piece_values["bishop"]
        elif type(piece) is Queen:
            evaluation += polarity * piece_values["queen"]
        elif type(piece) is King:
            evaluation += polarity * piece_values["king"]

    return evaluation


def piece_square_tables(piece_group):
    eval = 0
    for piece in piece_group:
        if piece.color == "white":
            eval -= piece.location_evaluation
        else:
            eval += piece.location_evaluation
    return eval


def static_evaluation(piece_group):
    evaluation = relative_piece_sum(piece_group) + piece_square_tables(piece_group)
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
